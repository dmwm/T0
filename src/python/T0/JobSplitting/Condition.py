"""
_Condition_

Splitting algorithm for PCL condition handling
"""

import logging
import threading
import time

from WMCore.WMBS.File import File

from WMCore.JobSplitting.JobFactory import JobFactory
from WMCore.DAOFactory import DAOFactory


class Condition(JobFactory):
    """
    Split jobs by set of files

    """
    def algorithm(self, groupInstance = None, jobInstance = None,
                  *args, **kwargs):
        """
        _algorithm_

        Different from any other job splitters in that
        we don't ever create any jobs.

        We just look at available files, process the information,
        store it in a different T0AST table and then mark the
        files as complete.

        Some other component will pick up from the info we wrote.

        """
        myThread = threading.currentThread()
        daoFactory = DAOFactory(package = "T0.WMBS",
                                logger = logging,
                                dbinterface = myThread.dbi)

        # only deal with closed fileset
        fileset = self.subscription.getFileset()
        fileset.load()
        if fileset.open:
            return

        # data discovery
        getFilesDAO = daoFactory(classname = "Subscriptions.GetAvailableConditionFiles")
        availableFiles = getFilesDAO.execute(self.subscription["id"])

        # nothing to do, stop immediately
        if len(availableFiles) == 0:
            return

        bindVarList = []
        for availableFile in availableFiles:
            bindVarList.append( { 'SUBSCRIPTION' : self.subscription["id"],
                                  'FILEID' : availableFile['id'],
                                  'RUN_ID' : availableFile['run_id'],
                                  'STREAM_ID' : availableFile['stream_id'] } )

        # save the information in T0AST and mark files complete
        insertPromptCalibrationFileDAO = daoFactory(classname = "JobSplitting.InsertPromptCalibrationFile")
        insertPromptCalibrationFileDAO.execute(bindVarList)

        return
