"""
_AlcaHarvest_

"""
import os
import time
import threading
import logging

from WMCore.WMBS.File import File

from WMCore.JobSplitting.JobFactory import JobFactory
from WMCore.DAOFactory import DAOFactory
from WMCore.Services.UUIDLib import makeUUID

class AlcaHarvest(JobFactory):
    """
    _AlcaHarvest_

    Under normal circumstance wait until the end of processing (input fileset
    is closed) and then issue a single job for all files.

    If the timeout parameter is specified and the current time is more than
    the runs stop time plus timeout, issue a job for all available files,
    then issue another job at the end of processing.

    """
    def algorithm(self, *args, **kwargs):
        """
        _algorithm_

        """
        self.jobNamePrefix = kwargs.get('jobNamePrefix', "AlcaHarvest")
        run = kwargs['runNumber']
        alcapromptdataset = kwargs['alcapromptdataset']
        timeout = kwargs['timeout']

        myThread = threading.currentThread()

        self.daoFactory = DAOFactory(package = "T0.WMBS",
                                     logger = logging,
                                     dbinterface = myThread.dbi)

        fileset = self.subscription.getFileset()
        fileset.load()

        if fileset.open:

            if timeout != None:

                haveAlcaHarvestJobGroupDAO = self.daoFactory(classname = "Subscriptions.HaveJobGroup")
                previousAlcaHarvest = haveAlcaHarvestJobGroupDAO.execute(self.subscription["id"])

                if not previousAlcaHarvest:

                    getRunStopTimeDAO = self.daoFactory(classname = "ConditionUpload.GetRunStopTime")
                    stopTime = getRunStopTimeDAO.execute(run, transaction = False)

                    if stopTime + timeout < time.time():

                        self.createJob(self.getInputFilesForJob(), alcapromptdataset)

        else:

            haveAvailableFileDAO = self.daoFactory(classname = "Subscriptions.HaveAvailableFile")
            availableFile = haveAvailableFileDAO.execute(self.subscription["id"])

            if availableFile:

                self.createJob(self.getInputFilesForJob(), alcapromptdataset)

        return

    def getInputFilesForJob(self):
        """
        _getInputFilesForJob_

        Just get all files in the fileset
        and the needed metadata

        """
        getAllFilesDAO = self.daoFactory(classname = "Subscriptions.GetAllFiles")
        return getAllFilesDAO.execute(self.subscription["id"])

    def createJob(self, fileList, alcapromptdataset):
        """
        _createJob_

        Create an alcaharvest job

        """
        self.newGroup()

        self.newJob(name = "%s-%s" % (self.jobNamePrefix, makeUUID()))

        if alcapromptdataset == "PromptCalibProdSiPixelAli":
            self.currentJob.addBaggageParameter("numberOfCores", 4)

        for fileInfo in fileList:
            f = File(id = fileInfo['id'],
                     lfn = fileInfo['lfn'])
            f.setLocation(fileInfo['location'], immediateSave = False)
            self.currentJob.addFile(f)
