"""
_Express_

Splitting algorithm for express processing.
"""

import logging
import threading

from WMCore.WMBS.File import File

from WMCore.JobSplitting.JobFactory import JobFactory
from WMCore.DAOFactory import DAOFactory
from WMCore.Services.UUID import makeUUID


class Express(JobFactory):
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
        self.jobNamePrefix = kwargs.get('jobNamePrefix', "Express")
        self.maxInputEvents = kwargs.get('maxInputEvents', 100)

        self.createdGroup = False

        myThread = threading.currentThread()
        daoFactory = DAOFactory(package = "T0.WMBS",
                                logger = logging,
                                dbinterface = myThread.dbi)

        # keep for later
        self.insertSplitLumisDAO = daoFactory(classname = "JobSplitting.InsertSplitLumis")

        # data discovery
        getFilesDAO = daoFactory(classname = "Subscriptions.GetAvailableExpressFiles")
        availableFiles = getFilesDAO.execute(self.subscription["id"])

        # nothing to do, stop immediately
        if len(availableFiles) == 0:
            return

        # sort by lumi
        streamersByLumi = {}
        for result in availableFiles:
            lumi = result['lumi']
            if streamersByLumi.has_key(lumi):
                streamersByLumi[lumi].append(result)
            else:
                streamersByLumi[lumi] = [ result ]

        self.defineJobs(streamersByLumi)

        return


    def defineJobs(self, streamersByLumi):
        """
        _defineJobs_

        schedule jobs

        """
        logging.debug("defineJobs(): Running...")

        splitLumis = []

        for lumi in sorted(streamersByLumi.keys()):

            lumiStreamerList = streamersByLumi[lumi]

            createdJob = False
            while len(lumiStreamerList) > 0:

                eventsTotal = 0
                streamerList = []

                for streamer in lumiStreamerList:

                    # if first streamer, always use it
                    if len(streamerList) == 0:
                        eventsTotal = streamer['events']
                        streamerList.append(streamer)
                    # otherwise calculate new totals and check if to use streamer
                    else:
                        newEventsTotal = eventsTotal + streamer['events']

                        if newEventsTotal <= self.maxInputEvents:
                            eventsTotal = newEventsTotal
                            streamerList.append(streamer)

                if createdJob:
                    splitLumis.append( { 'SUB' : self.subscription["id"],
                                         'LUMI' : lumi } )

                self.createJob(streamerList)
                createdJob = True

                for streamer in streamerList:
                    lumiStreamerList.remove(streamer)

        if len(splitLumis) > 0:
            self.insertSplitLumisDAO.execute(binds = splitLumis)

        return


    def createJob(self, streamerList):
        """
        _createJob_

        create an express job processing
        the passed in list of streamers

        """
        if not self.createdGroup:
            self.newGroup()
            self.createdGroup = True

        self.newJob(name = "%s-%s" % (self.jobNamePrefix, makeUUID()))

        for streamer in streamerList:
            f = File(id = streamer['id'])
            f.setLocation(streamer['location'], immediateSave = False)
            self.currentJob.addFile(f)
