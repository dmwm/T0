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
        self.maxInputEvents = kwargs['maxInputEvents']
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
        getClosedEmptyLumisFromChildSubDAO = daoFactory(classname = "JobSplitting.GetClosedEmptyLumisFromChildSub")
        getCompletedLumisFromChildSubDAO = daoFactory(classname = "JobSplitting.GetCompletedLumisFromChildSub")

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

        # highest lumi with a job
        maxLumiWithJob = 0
        if lumiList[0] > 1:
            maxLumiWithJob = maxLumiWithJobDAO.execute(self.subscription["id"])

        # consistency check
        if lumiList[0] <= maxLumiWithJob:
            logging.error("ERROR: finding data that can't be there, bailing out...")
            return

        # do we have lumi holes ?
        detectEmptyLumis = False
        detectCompleteLumis = False
        lumi = maxLumiWithJob + 1
        while lumi in lumiList:
            lumi += 1
        if lumi < lumiList[-1]:
            detectEmptyLumis = True

        # empty and closed lumis
        emptyLumis = []
        if detectEmptyLumis:

            emptyLumis = getClosedEmptyLumisFromChildSubDAO.execute(self.subscription["id"], maxLumiWithJob)

            # do we still have lumi holes ?
            lumi = maxLumiWithJob + 1
            while lumi in lumiList or lumi in emptyLumis:
                lumi += 1
            if lumi < lumiList[-1]:
                detectCompleteLumis = True

        # lumis for which repacking is complete
        completeLumis = []
        if detectCompleteLumis:
            completeLumis = getCompletedLumisFromChildSubDAO.execute(self.subscription["id"], maxLumiWithJob)

        # figure out lumi range to create jobs for
        filesByLumi = {}
        firstLumi = maxLumiWithJob + 1
        lastLumi = lumiList[-1]
        for lumi in range(firstLumi, lastLumi + 1):
            if (lumi in lumiList) or (lumi in emptyLumis) or (lumi in completeLumis):
                filesByLumi[lumi] = []
            else:
                break

        # figure out what data to create jobs for
        for fileInfo in availableFiles:
            lumi = fileInfo['first_lumi']
            if filesByLumi.has_key(lumi):
                filesByLumi[lumi].append(fileInfo)

        # check if fileset is closed
        fileset = self.subscription.getFileset()
        fileset.load()

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
                    self.createJob(jobFileList)
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

                            if newSizeTotal <= self.maxEdmSize and \
                                   newEventsTotal <= self.maxInputEvents:
                                eventsTotal = newEventsTotal
                                sizeTotal = newSizeTotal
                                fileList.append(fileInfo)

                    self.createJob(fileList, errorDataset = True)

                    for fileInfo in fileList:
                        lumiFileList.remove(fileInfo)

            elif lumiSizeTotal >= self.maxInputSize or \
                     lumiEventsTotal >= self.maxInputEvents or \
                     lumiInputFiles >= self.maxInputFiles:

                # merge what we have to preserve order
                if len(jobFileList) > 0:
                    self.createJob(jobFileList)
                    jobSizeTotal = 0
                    jobEventsTotal = 0
                    jobInputFiles = 0
                    jobFileList = []

                # then issue merge on new lumi
                self.createJob(lumiFileList)

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

                    self.createJob(jobFileList)
                    jobSizeTotal = lumiSizeTotal
                    jobEventsTotal = lumiEventsTotal
                    jobInputFiles = lumiInputFiles
                    jobFileList = lumiFileList


                # over limits with new file, below minimum without it
                # still below override limits (and below event limit)
                # add file, issue merge job (too large)
                elif newSizeTotal <= self.maxOverSize and \
                         newEventsTotal <= self.maxInputEvents:

                    jobFileList.extend(lumiFileList)
                    self.createJob(jobFileList)
                    jobSizeTotal = 0
                    jobEventsTotal = 0
                    jobInputFiles = 0
                    jobFileList = []

                # over limits with new file, below minimum without it
                # over override limit or event limit with new file
                # issue merge job (too small)
                else:

                    self.createJob(jobFileList)
                    jobSizeTotal = lumiSizeTotal
                    jobEventsTotal = lumiEventsTotal
                    jobInputFiles = lumiInputFiles
                    jobFileList = [lumiFileList]

        # finish out leftovers if we are in closeout
        if len(jobFileList) > 0 and not filesetOpen:
            self.createJob(jobFileList)

        return


    def createJob(self, fileList, errorDataset = False):
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

        for fileInfo in fileList:
            f = File(id = fileInfo['id'],
                     lfn = fileInfo['lfn'])
            f.setLocation(fileInfo['location'], immediateSave = False)
            self.currentJob.addFile(f)

