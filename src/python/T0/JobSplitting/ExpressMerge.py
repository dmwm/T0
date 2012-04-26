"""
_ExpressMerge_

Splitting algorithm for express merging
"""

import logging
import threading
import time

from WMCore.WMBS.File import File

from WMCore.JobSplitting.JobFactory import JobFactory
from WMCore.DAOFactory import DAOFactory
from WMCore.Services.UUID import makeUUID


class ExpressMerge(JobFactory):
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
        self.jobNamePrefix = kwargs.get('jobNamePrefix', "ExpressMerge")
        self.maxInputSize = kwargs['maxInputSize']
        self.maxInputFiles = kwargs['maxInputFiles']
        self.maxLatency = kwargs['maxLatency']
        self.currentTime = time.time()

        self.createdGroup = False

        myThread = threading.currentThread()
        daoFactory = DAOFactory(package = "T0.WMBS",
                                logger = logging,
                                dbinterface = myThread.dbi)

        # data discovery
        getFilesDAO = daoFactory(classname = "Subscriptions.GetAvailableExpressMergeFiles")
        availableFiles = getFilesDAO.execute(self.subscription["id"])

        # nothing to do, stop immediately
        if len(availableFiles) == 0:
            return

        # sort by lumi
        filesByLumi = {}
        for result in availableFiles:
            lumi = result['lumi']
            if filesByLumi.has_key(lumi):
                filesByLumi[lumi].append(result)
            else:
                filesByLumi[lumi] = [ result ]

        self.defineJobs(filesByLumi)

        return


    def defineJobs(self, filesByLumi):
        """
        _defineJobs_

        schedule jobs

        """
        logging.debug("defineJobs(): Running...")

        #
        # actual scheduling algorith
        #
        # criteria:
        #     1. a lumi section should not sit around too long, waiting to get merged
        #     2. if possible, we want to merge in order of lumi sections (no holes)
        #     3. avoid too many small files (merge as many lumi sections as possible)
        #     4. don't merge too many lumi sections as the jobs run too long
        #     5. last, don't produce too big files
        #
        #     merge whatever we have (without holes) if oldest lumi section older than self.maxLatency
        #     if self.maxLatency is 0, merge lumi by lumi
        #

        lastLumi = 0
        jobSizeTotal = 0
        jobFileList = []

        for lumi in sorted(filesByLumi.keys()):

            lumiFileList = filesByLumi[lumi]

            # find oldest file in the lumi
            lumiDoneTime = 0
            for fileInfo in lumiFileList:
                if fileInfo['insert_time'] > lumiDoneTime:
                    lumiDoneTime = fileInfo['insert_time']
            lumiAge = self.currentTime - lumiDoneTime

            # calculate lumi size and new total size and file count
            lumiSizeTotal = 0
            for fileInfo in lumiFileList:
                lumiSizeTotal += fileInfo['filesize']

            newSizeTotal = jobSizeTotal + lumiSizeTotal
            newFileCount = len(jobFileList) + len(lumiFileList)

            # first lumi, if not old enough bail out
            if len(jobFileList) == 0:
                if lumiAge > self.maxLatency:
                    jobFileList.extend(lumiFileList)
                    lastLumi = lumi
                    jobSizeTotal = lumiSizeTotal
                else:
                    break
            # if self.maxLatency 0, just expressmerge lumi by lumi
            elif self.maxLatency == 0:
                self.createJob(jobFileList)
                jobFileList = lumiFileList
                lastLumi = lumi
                jobSizeTotal = lumiSizeTotal
            # observe strict lumi order and sequence broken => expressmerge
            # triggers new age check on next out of sequence lumi
            # bail if not old enough
            elif lumi != lastLumi + 1:
                self.createJob(jobFileList)
                if lumiAge > self.maxLatency:
                    jobFileList = lumiFileList
                    lastLumi = lumi
                    jobSizeTotal = lumiSizeTotal
                else:
                    jobFileList = []
                    break
            # if below limits just add to expressmerge job
            elif newFileCount <= self.maxInputFiles and \
                     newSizeTotal <= self.maxInputSize:
                jobFileList.extend(lumiFileList)
                lastLumi = lumi
                jobSizeTotal = newSizeTotal
            # over limits => expressmerge
            else:
                self.createJob(jobFileList)
                jobFileList = lumiFileList
                lastLumi = lumi
                jobSizeTotal = lumiSizeTotal

        # sequential leftovers that are old enough
        if len(jobFileList) > 0:
            self.createJob(jobFileList)

        return


    def createJob(self, fileList):
        """
        _createJob_

        create an express merge job for
        the passed in list of files

        """
        if not self.createdGroup:
            self.newGroup()
            self.createdGroup = True

        self.newJob(name = "%s-%s" % (self.jobNamePrefix, makeUUID()))

        for fileInfo in fileList:
            f = File(id = fileInfo['id'],
                     lfn = fileInfo['lfn'])
            f.setLocation(fileInfo['location'], immediateSave = False)
            self.currentJob.addFile(f)
