"""
_RepackMerge_

Splitting algorithm for express merging
"""

import time
import logging
import threading

from WMCore.WMBS.File import File

from WMCore.JobSplitting.JobFactory import JobFactory
from WMCore.DAOFactory import DAOFactory
from WMCore.Services.UUIDLib import makeUUID


class RepackMerge(JobFactory):
    """
    Split jobs by set of files

    """
    def algorithm(self, groupInstance = None, jobInstance = None,
                  *args, **kwargs):
        """
        _algorithm_

        A file based splitting algorithm

        """
        # extract some global scheduling parameters
        self.jobNamePrefix = kwargs.get('jobNamePrefix', "RepackMerge")
        self.minInputSize = kwargs['minInputSize']
        self.maxInputSize = kwargs['maxInputSize']
        self.maxInputEvents = kwargs['maxInputEvents']
        self.maxInputFiles = kwargs['maxInputFiles']
        self.maxEdmSize = kwargs['maxEdmSize']
        self.maxOverSize = kwargs['maxOverSize']
        self.maxLatency = kwargs['maxLatency']

        # catch configuration errors
        if self.maxOverSize > self.maxEdmSize:
            self.maxOverSize = self.maxEdmSize

        self.currentTime = time.time()

        self.createdGroup = False

        myThread = threading.currentThread()
        daoFactory = DAOFactory(package = "T0.WMBS",
                                logger = logging,
                                dbinterface = myThread.dbi)

        # data discovery
        getAvailableFilesDAO = daoFactory(classname = "Subscriptions.GetAvailableRepackMergeFiles")
        availableFiles = getAvailableFilesDAO.execute(self.subscription["id"])

        # nothing to do, stop immediately
        if len(availableFiles) == 0:
            return

        # data discovery for already used lumis
        getUsedLumisDAO = daoFactory(classname = "Subscriptions.GetUsedLumis")
        usedLumis = getUsedLumisDAO.execute(self.subscription["id"], True)

        # empty lumis (as declared by StorageManager) are treated the
        # same way as used lumis, ie. we process around them
        getEmptyLumisDAO = daoFactory(classname = "Subscriptions.GetLumiHolesForRepackMerge")
        usedLumis |= getEmptyLumisDAO.execute(self.subscription["id"])

        # sort available files by lumi
        availableFileLumiDict = {}
        for result in availableFiles:
            for lumi in range(result['first_lumi'], 1+result['last_lumi']):
                if lumi not in availableFileLumiDict:
                    availableFileLumiDict[lumi] = []
                if lumi == result['first_lumi']:
                    availableFileLumiDict[lumi].append(result)

        # loop through lumis in order
        haveLumiHole = False
        filesByLumi = {}
        maxUsedLumi = max(usedLumis) if usedLumis else 0
        for lumi in range(1, 1+max(maxUsedLumi,max(availableFileLumiDict.keys()))):

            # lumi contains data => remember it for potential processing
            if lumi in availableFileLumiDict:

                filesByLumi[lumi] = availableFileLumiDict[lumi]

            # lumi is used and we have data => trigger processing
            elif lumi in usedLumis:

                if len(filesByLumi) > 0:

                    if haveLumiHole:
                        # if lumi hole check for maxLatency first
                        if self.getDataAge(filesByLumi) > self.maxLatency:
                            self.defineJobs(filesByLumi, True)
                            filesByLumi = {}
                        # if maxLatency not met ignore data for now
                        else:
                            filesByLumi = {}
                    else:
                        self.defineJobs(filesByLumi, True)
                        filesByLumi = {}

                # if we had a lumi hole it is now not relevant anymore
                # the next data will have a used lumi in front of it
                haveLumiHole = False

            # lumi has no data and isn't used, ie. we have a lumi hole
            # also has an impact on how to handle later data
            else:

                if len(filesByLumi) > 0:

                    # forceClose if maxLatency trigger is met
                    if self.getDataAge(filesByLumi) > self.maxLatency:
                        self.defineJobs(filesByLumi, True)
                        filesByLumi = {}
                    # follow the normal thresholds, but only if
                    # there is no lumi hole in front of the data
                    elif not haveLumiHole:
                        self.defineJobs(filesByLumi, False)
                        filesByLumi = {}
                    # otherwise ignore the data for now
                    else:
                        filesByLumi = {}

                haveLumiHole = True

        # now handle whatever data is still left (at the high end of the lumi range)
        if haveLumiHole:
            if self.getDataAge(filesByLumi) > self.maxLatency:
                self.defineJobs(filesByLumi, True)
        else:
            fileset = self.subscription.getFileset()
            fileset.load()
            self.defineJobs(filesByLumi, not fileset.open)

        return

    def getDataAge(self, filesByLumi):
        """
        _getDataAge_

        Return age of youngest streamer in filesByLumi
        """
        maxInsertTime = 0
        for filesInfos in list(filesByLumi.values()):
            for fileInfo in filesInfos:
                if fileInfo['insert_time'] > maxInsertTime:
                    maxInsertTime = fileInfo['insert_time']

        return self.currentTime - maxInsertTime

    def defineJobs(self, filesByLumi, forceClose):
        """
        _defineJobs_

        schedule jobs

        """
        logging.debug("defineJobs(): Running...")

        jobSizeTotal = 0
        jobEventsTotal = 0
        jobInputFiles = 0
        jobFileList = []

        for lumi in sorted(filesByLumi.keys()):

            lumiFileList = filesByLumi[lumi]
            if len(lumiFileList) == 0:
                continue

            # calculate lumi size and event count
            lumiSizeTotal = 0
            lumiEventsTotal = 0
            lumiInputFiles = 0
            for fileInfo in lumiFileList:
                lumiEventsTotal += fileInfo['events']
                lumiSizeTotal += fileInfo['filesize']
                lumiInputFiles += 1

            # lumi is larger than edm size limit
            #
            # => split up lumi and merge individual parts
            #
            if lumiSizeTotal > self.maxEdmSize:

                # merge what we have to preserve order
                if len(jobFileList) > 0:
                    self.createJob(jobFileList, jobSizeTotal)
                    jobSizeTotal = 0
                    jobEventsTotal = 0
                    jobInputFiles = 0
                    jobFileList = []

                while len(lumiFileList) > 0:

                    eventsTotal = 0
                    sizeTotal = 0
                    fileList = []
                    for fileInfo in lumiFileList:

                        # if first file, always use it
                        if len(fileList) == 0:
                            eventsTotal = fileInfo['events']
                            sizeTotal = fileInfo['filesize']
                            fileList.append(fileInfo)

                        # otherwise calculate new totals and check if to use file
                        else:

                            newEventsTotal = eventsTotal + fileInfo['events']
                            newSizeTotal = sizeTotal + fileInfo['filesize']

                            if newSizeTotal <= self.maxEdmSize:

                                eventsTotal = newEventsTotal
                                sizeTotal = newSizeTotal
                                fileList.append(fileInfo)

                    self.createJob(fileList, eventsTotal, errorDataset = True)

                    for fileInfo in fileList:
                        lumiFileList.remove(fileInfo)

            elif lumiSizeTotal > self.maxInputSize or \
                    lumiEventsTotal > self.maxInputEvents or \
                    lumiInputFiles > self.maxInputFiles:

                # merge what we have to preserve order
                if len(jobFileList) > 0:
                    self.createJob(jobFileList, jobSizeTotal)
                    jobSizeTotal = 0
                    jobEventsTotal = 0
                    jobInputFiles = 0
                    jobFileList = []

                # then issue merge on new lumi
                self.createJob(lumiFileList, lumiSizeTotal)

            else:

                newSizeTotal = jobSizeTotal + lumiSizeTotal
                newEventsTotal = jobEventsTotal + lumiEventsTotal
                newInputFiles = jobInputFiles + lumiInputFiles

                # still safe with new file, just add it
                if newSizeTotal <= self.maxInputSize and \
                        newEventsTotal <= self.maxInputEvents and \
                        newInputFiles <= self.maxInputFiles:

                    jobSizeTotal = newSizeTotal
                    jobEventsTotal = newEventsTotal
                    jobInputFiles = newInputFiles
                    jobFileList.extend(lumiFileList)

                # over limits with new file, over minimum without it
                # issue merge job (regular)
                elif jobSizeTotal > self.minInputSize:

                    self.createJob(jobFileList, jobSizeTotal)
                    jobSizeTotal = lumiSizeTotal
                    jobEventsTotal = lumiEventsTotal
                    jobInputFiles = lumiInputFiles
                    jobFileList = lumiFileList


                # over limits with new file, below minimum without it
                # still below override limits (and below event limit)
                # add file, issue merge job (too large)
                elif newSizeTotal <= self.maxOverSize:

                    jobFileList.extend(lumiFileList)
                    self.createJob(jobFileList, jobSizeTotal)
                    jobSizeTotal = 0
                    jobEventsTotal = 0
                    jobInputFiles = 0
                    jobFileList = []

                # over limits with new file, below minimum without it
                # over override limit or event limit with new file
                # issue merge job (too small)
                else:

                    self.createJob(jobFileList, jobSizeTotal)
                    jobSizeTotal = lumiSizeTotal
                    jobEventsTotal = lumiEventsTotal
                    jobInputFiles = lumiInputFiles
                    jobFileList = lumiFileList

        # finish out leftovers if we are in closeout
        if len(jobFileList) > 0 and forceClose:
            self.createJob(jobFileList, jobSizeTotal)

        return


    def createJob(self, fileList, jobSize, errorDataset = False):
        """
        _createJob_

        create a repack merge job for
        the passed in list of files

        """
        # find largest file
        largestFile = 0
        for fileInfo in fileList:
            largestFile = max(largestFile, fileInfo['filesize'])

        # calculate number of cores based on disk usage
        numberOfCores = 1 + (int)((jobSize+largestFile)/(20*1000*1000*1000))

        # jobs requesting more than 8 cores would never run
        if numberOfCores > 8:
            self.markFailed(streamerList)
            return

        if not self.createdGroup:
            self.newGroup()
            self.createdGroup = True

        self.newJob(name = "%s-%s" % (self.jobNamePrefix, makeUUID()))

        for fileInfo in fileList:
            f = File(id = fileInfo['id'],
                     lfn = fileInfo['lfn'])
            f.setLocation(fileInfo['location'], immediateSave = False)
            self.currentJob.addFile(f)

        if errorDataset:
            self.currentJob.addBaggageParameter("useErrorDataset", True)

        # allow large (single lumi) repackmerge to use multiple cores
        if numberOfCores > 1:
            self.currentJob.addBaggageParameter("numberOfCores", numberOfCores)

        # job time based on
        #  - 5 min initialization
        #  - 5MB/s merge speed
        #  - checksum calculation at 5MB/s
        #  - stageout at 5MB/s
        # job disk based on
        #  - input for largest file on local disk
        #  - output on local disk (factor 1)
        jobTime = 300 + (jobSize*3)/5000000
        self.currentJob.addResourceEstimates(jobTime = jobTime,
                                             disk = (jobSize+largestFile)/1024,
                                             memory = 1000)

        return
