"""
_RepackMerge_

Splitting algorithm for express merging
"""

import logging
import threading
import time

from WMCore.WMBS.File import File

from WMCore.JobSplitting.JobFactory import JobFactory
from WMCore.DAOFactory import DAOFactory
from WMCore.Services.UUID import makeUUID


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

        self.maxInputFiles = kwargs['maxInputFiles']

        self.maxEdmSize = kwargs['maxEdmSize']
        self.maxOverSize = kwargs['maxOverSize']

        # catch configuration errors
        if self.maxOverSize > self.maxEdmSize:
            self.maxOverSize = self.maxEdmSize

        self.createdGroup = False

        myThread = threading.currentThread()
        daoFactory = DAOFactory(package = "T0.WMBS",
                                logger = logging,
                                dbinterface = myThread.dbi)

        maxLumiWithJobDAO = daoFactory(classname = "Subscriptions.MaxLumiWithJob")
        getGoodLumiHolesDAO = daoFactory(classname = "JobSplitting.GetGoodLumiHoles")

        # highest lumi with a job
        maxLumiWithJob = maxLumiWithJobDAO.execute(self.subscription["id"])

        logging.debug("DEBUG Sub %d, maxLumiWithJob = %d" % (self.subscription["id"], maxLumiWithJob))

        # find good lumi holes (needs to be done before data discovery)
        goodLumiHoles = getGoodLumiHolesDAO.execute(self.subscription["id"], maxLumiWithJob)

        logging.debug("DEBUG Sub %d, goodLumiHoles = %s" % (self.subscription["id"], sorted(goodLumiHoles)))

        # data discovery
        getFilesDAO = daoFactory(classname = "Subscriptions.GetAvailableRepackMergeFiles")
        availableFiles = getFilesDAO.execute(self.subscription["id"])

        # nothing to do, stop immediately
        if len(availableFiles) == 0:
            return

        # lumis we have data for
        lumiList = set([])
        for result in availableFiles:
            for lumi in range(result['first_lumi'], result['last_lumi'] + 1):
                lumiList.add(lumi)
        lumiList = sorted(list(lumiList))

        logging.debug("DEBUG Sub %d, lumiList = %s" % (self.subscription["id"], lumiList))

        # check if fileset is closed
        fileset = self.subscription.getFileset()
        fileset.load()

        # extended lumi range for job creation
        firstLumi = maxLumiWithJob + 1
        lastLumi = lumiList[-1]

        # consistency check (ignore at end of run)
        if lumiList[0] <= maxLumiWithJob:
            if fileset.open:
                logging.error("ERROR: finding data that can't be there, bailing out...")
                return
            else:
                logging.info("WARNING: finding data that can't be there, fileset is closed, merge anyways...")
                firstLumi = lumiList[0]

        # narrow down lumi range for job creation
        filesByLumi = {}
        for lumi in range(firstLumi, lastLumi + 1):
            if (lumi in lumiList) or (lumi in goodLumiHoles):
                filesByLumi[lumi] = []
            else:
                break

        # figure out what data to create jobs for
        for fileInfo in availableFiles:
            lumi = fileInfo['first_lumi']
            if filesByLumi.has_key(lumi):
                filesByLumi[lumi].append(fileInfo)

        logging.debug("DEBUG Sub %d, create jobs for lumis = %s" % (self.subscription["id"], sorted(filesByLumi.keys())))

        self.defineJobs(filesByLumi, fileset.open)

        return


    def defineJobs(self, filesByLumi, filesetOpen):
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
        if len(jobFileList) > 0 and not filesetOpen:
            self.createJob(jobFileList, jobSizeTotal)

        return


    def createJob(self, fileList, jobSize, errorDataset = False):
        """
        _createJob_

        create a repack merge job for
        the passed in list of files

        """
        if not self.createdGroup:
            self.newGroup()
            self.createdGroup = True

        self.newJob(name = "%s-%s" % (self.jobNamePrefix, makeUUID()))

        if errorDataset:
            self.currentJob.addBaggageParameter("useErrorDataset", True)

        largestFile = 0
        for fileInfo in fileList:
            largestFile = max(largestFile, fileInfo['filesize'])
            f = File(id = fileInfo['id'],
                     lfn = fileInfo['lfn'])
            f.setLocation(fileInfo['location'], immediateSave = False)
            self.currentJob.addFile(f)

        # job time based on
        #   - 5 min initialization
        #   - 5MB/s merge speed
        #   - checksum calculation at 5MB/s
        #   - stageout at 5MB/s
        # job disk based on
        #  - input for largest file on local disk
        #  - output on local disk (factor 1)
        jobTime = 300 + (jobSize*3)/5000000
        self.currentJob.addResourceEstimates(jobTime = jobTime,
                                             disk = (jobSize+largestFile)/1024,
                                             memory = 1000)

        return
