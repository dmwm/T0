"""
_Repack_

Splitting algorithm for repacking.
"""

import time
import logging
import threading

from WMCore.WMBS.File import File

from WMCore.JobSplitting.JobFactory import JobFactory
from WMCore.DAOFactory import DAOFactory
from WMCore.Services.UUIDLib import makeUUID


class Repack(JobFactory):
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
        self.jobNamePrefix = kwargs.get('jobNamePrefix', "Repack")
        self.maxSizeSingleLumi = kwargs['maxSizeSingleLumi']
        self.maxSizeMultiLumi = kwargs['maxSizeMultiLumi']
        self.maxInputEvents = kwargs['maxInputEvents']
        self.maxInputFiles = kwargs['maxInputFiles']
        self.maxLatency = kwargs['maxLatency']

        self.currentTime = time.time()

        self.createdGroup = False

        timePerEvent, sizePerEvent, memoryRequirement = \
                    self.getPerformanceParameters(kwargs.get('performance', {}))
        
        myThread = threading.currentThread()
        daoFactory = DAOFactory(package = "T0.WMBS",
                                logger = logging,
                                dbinterface = myThread.dbi)

        # keep for later
        self.insertSplitLumisDAO = daoFactory(classname = "JobSplitting.InsertSplitLumis")

        # data discovery
        getAvailableFilesDAO = daoFactory(classname = "Subscriptions.GetAvailableRepackFiles")
        availableFiles = getAvailableFilesDAO.execute(self.subscription["id"])

        # nothing to do, stop immediately
        if len(availableFiles) == 0:
            return

        # data discovery for already used lumis
        getUsedLumisDAO = daoFactory(classname = "Subscriptions.GetUsedLumis")
        usedLumis = getUsedLumisDAO.execute(self.subscription["id"], False)

        # empty lumis (as declared by StorageManager) are treated the
        # same way as used lumis, ie. we process around them
        getEmptyLumisDAO = daoFactory(classname = "Subscriptions.GetLumiHolesForRepack")
        usedLumis |= getEmptyLumisDAO.execute(self.subscription["id"])

        # sort available files by lumi
        availableFileLumiDict = {}
        for result in availableFiles:
            lumi = result['lumi']
            if not lumi in availableFileLumiDict:
                availableFileLumiDict[lumi] = []
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
                            self.defineJobs(filesByLumi, True, memoryRequirement)
                            filesByLumi = {}
                        # if maxLatency not met ignore data for now
                        else:
                            filesByLumi = {}
                    else:
                        self.defineJobs(filesByLumi, True, memoryRequirement)
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
                        self.defineJobs(filesByLumi, True, memoryRequirement)
                        filesByLumi = {}
                    # follow the normal thresholds, but only if
                    # there is no lumi hole in front of the data
                    elif not haveLumiHole:
                        self.defineJobs(filesByLumi, False, memoryRequirement)
                        filesByLumi = {}
                    # otherwise ignore the data for now
                    else:
                        filesByLumi = {}

                haveLumiHole = True

        # now handle whatever data is still left (at the high end of the lumi range)
        if haveLumiHole:
            if self.getDataAge(filesByLumi) > self.maxLatency:
                self.defineJobs(filesByLumi, True, memoryRequirement)
        else:
            fileset = self.subscription.getFileset()
            fileset.load()
            self.defineJobs(filesByLumi, not fileset.open, memoryRequirement)

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

    def defineJobs(self, streamersByLumi, forceClose, memoryRequirement):
        """
        _defineStrictJobs_

        schedule jobs

        """
        logging.debug("defineJobs(): Running...")

        jobSizeTotal = 0
        jobEventsTotal = 0
        jobStreamerList = []

        splitLumis = []

        for lumi in sorted(streamersByLumi.keys()):

            lumiStreamerList = streamersByLumi[lumi]
            if len(lumiStreamerList) == 0:
                continue

            # calculate lumi size and event count
            lumiSizeTotal = 0
            lumiEventsTotal = 0
            for streamer in lumiStreamerList:
                lumiEventsTotal += streamer['events']
                lumiSizeTotal += streamer['filesize']

            # lumi is larger than split limits
            #
            # => handle lumi individually and split
            #
            if lumiSizeTotal > self.maxSizeSingleLumi or \
                   lumiEventsTotal > self.maxInputEvents:

                # repack what we have to preserve order
                if len(jobStreamerList) > 0:
                    self.createJob(jobStreamerList, jobEventsTotal, jobSizeTotal, memoryRequirement)
                    jobSizeTotal = 0
                    jobEventsTotal = 0
                    jobStreamerList = []

                createdJobs = 0
                nFiles = len(lumiStreamerList)
                while len(lumiStreamerList) > 0:

                    eventsTotal = 0
                    sizeTotal = 0
                    streamerList = []
                    for streamer in lumiStreamerList:

                        # if first streamer, always use it
                        if len(streamerList) == 0:
                            eventsTotal = streamer['events']
                            sizeTotal = streamer['filesize']
                            streamerList.append(streamer)

                        # otherwise calculate new totals and check if to use streamer
                        else:
                            newEventsTotal = eventsTotal + streamer['events']
                            newSizeTotal = sizeTotal + streamer['filesize']                        

                            if newSizeTotal <= self.maxSizeSingleLumi and \
                                    newEventsTotal <= self.maxInputEvents:

                                eventsTotal = newEventsTotal
                                sizeTotal = newSizeTotal
                                streamerList.append(streamer)

                    self.createJob(streamerList, eventsTotal, sizeTotal, memoryRequirement)

                    for streamer in streamerList:
                        lumiStreamerList.remove(streamer)

                    createdJobs += 1

                if createdJobs > 1:
                    splitLumis.append( { 'SUB' : self.subscription["id"],
                                         'LUMI' : lumi, 'NFILES' : nFiles } )

            # lumi is smaller than split limits
            # check if it can be combined with previous lumi(s)
            #
            # yes => just add lumi to job (with an additional order check)
            #
            # no => issue job for previous lumi(s), save current for next job
            #
            else:

                newSizeTotal = jobSizeTotal + lumiSizeTotal
                newEventsTotal = jobEventsTotal + lumiEventsTotal
                newInputfiles = len(jobStreamerList) + len(lumiStreamerList)

                # always take the first one
                if len(jobStreamerList) == 0:

                    jobSizeTotal = newSizeTotal
                    jobEventsTotal = newEventsTotal
                    jobStreamerList.extend(lumiStreamerList)

                # still safe with new lumi, just add it
                elif newSizeTotal <= self.maxSizeMultiLumi and \
                        newEventsTotal <= self.maxInputEvents and \
                        newInputfiles <= self.maxInputFiles:

                    jobSizeTotal = newSizeTotal
                    jobEventsTotal = newEventsTotal
                    jobStreamerList.extend(lumiStreamerList)

                # over limits with new lumi, issue repack job
                else:

                    self.createJob(jobStreamerList, jobEventsTotal, jobSizeTotal, memoryRequirement)

                    jobSizeTotal = lumiSizeTotal
                    jobEventsTotal = lumiEventsTotal
                    jobStreamerList = lumiStreamerList

        # if we are in closeout issue repack job for leftovers
        if len(jobStreamerList) > 0 and forceClose:
            self.createJob(jobStreamerList, jobEventsTotal, jobSizeTotal, memoryRequirement)

        if len(splitLumis) > 0:
            self.insertSplitLumisDAO.execute(binds = splitLumis)

        return


    def createJob(self, streamerList, jobEvents, jobSize, memoryRequirement):
        """
        _createJob_

        """
        # find largest file
        largestFile = 0
        for streamer in streamerList:
            largestFile = max(largestFile, streamer['filesize'])

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

        for streamer in streamerList:
            f = File(id = streamer['id'],
                     lfn = streamer['lfn'])
            f.setLocation(streamer['location'], immediateSave = False)
            self.currentJob.addFile(f)

        # allow large (single lumi) repack to use multiple cores
        if numberOfCores > 1:
            self.currentJob.addBaggageParameter("numberOfCores", numberOfCores)

        # job time based on
        #  - 5 min initialization
        #  - 1.5MB/s repack speed
        #  - checksum calculation at 5MB/s
        #  - stageout at 5MB/s
        # job disk based on
        #  - input for largest file on local disk
        #  - output on local disk (factor 1)
        jobTime = 300 + jobSize/1500000 + (jobSize*2)/5000000
        self.currentJob.addResourceEstimates(jobTime = jobTime,
                                             disk = (jobSize+largestFile)/1024,
                                             memory = memoryRequirement)

        return


    def markFailed(self, streamerList):
        """
        _markFailed_

        mark all streamers as failed
        """
        fileList = []
        for streamer in streamerList:
            fileList.append( File(id = streamer['id'],
                                  lfn = streamer['lfn']) )
        self.subscription.failFiles(fileList)

        return
