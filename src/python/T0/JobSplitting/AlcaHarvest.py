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
from WMCore.Services.UUID import makeUUID

class AlcaHarvest(JobFactory):
    """
    _AlcaHarvest_

    Under normal circumstance wait until the end of processing (input fileset
    is closed) and then issue a single job for all files.

    If the timeout parameter is specified and the current time is more than
    the runs end_time plus timeout, issue a job for all available files,
    then issue another job at the end of processing.

    """
    def algorithm(self, *args, **kwargs):
        """
        _algorithm_

        """
        self.jobNamePrefix = kwargs.get('jobNamePrefix', "AlcaHarvest")
        run = kwargs['runNumber']
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

                    getRunEndTimeDAO = self.daoFactory(classname = "ConditionUpload.GetRunEndTime")
                    endTime = getRunEndTimeDAO.execute(run, transaction = False)

                    if endTime + timeout < time.time():

                        self.createJob(self.getInputFilesForJob())

        else:

            haveAvailableFileDAO = self.daoFactory(classname = "Subscriptions.HaveAvailableFile")
            availableFile = haveAvailableFileDAO.execute(self.subscription["id"])

            if availableFile:

                self.createJob(self.getInputFilesForJob())

        return

    def getInputFilesForJob(self):
        """
        _getInputFilesForJob_

        Just get all files in the fileset
        and the needed metadata

        """
        getAllFilesDAO = self.daoFactory(classname = "Subscriptions.GetAllFiles")
        return getAllFilesDAO.execute(self.subscription["id"])


    def createJob(self, fileList):
        """
        _createJob_

        Create an alcaharvest job

        """
        self.newGroup()

        self.newJob(name = "%s-%s" % (self.jobNamePrefix, makeUUID()))

        for fileInfo in fileList:
            f = File(id = fileInfo['id'],
                     lfn = fileInfo['lfn'])
            f.setLocation(fileInfo['location'], immediateSave = False)
            self.currentJob.addFile(f)

        if 'X509_USER_PROXY' in os.environ:
            self.currentJob['proxyPath'] = os.environ['X509_USER_PROXY']
