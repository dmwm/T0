"""
_Express_

Splitting algorithm for express processing.
"""

import logging
import threading

from WMCore.WMBS.File import File

from WMCore.JobSplitting.JobFactory import JobFactory
from WMCore.DAOFactory import DAOFactory
from WMCore.Services.UUIDLib import makeUUID


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
        self.maxInputRate = kwargs['maxInputRate']
        self.maxInputEvents = kwargs['maxInputEvents']

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
        getFilesDAO = daoFactory(classname = "Subscriptions.GetAvailableExpressFiles")
        availableFiles = getFilesDAO.execute(self.subscription["id"])

        # nothing to do, stop immediately
        if len(availableFiles) == 0:
            return

        # sort by lumi
        streamersByLumi = {}
        for result in availableFiles:
            lumi = result['lumi']
            if lumi in streamersByLumi:
                streamersByLumi[lumi].append(result)
            else:
                streamersByLumi[lumi] = [ result ]

        self.defineJobs(streamersByLumi, timePerEvent, sizePerEvent, memoryRequirement)

        return


    def defineJobs(self, streamersByLumi, timePerEvent, sizePerEvent, memoryRequirement):
        """
        _defineJobs_

        schedule jobs

        """
        logging.debug("defineJobs(): Running...")

        splitLumis = []

        for lumi in sorted(streamersByLumi.keys()):

            lumiStreamerList = streamersByLumi[lumi]

            # calculate lumi size and event count
            lumiSizeTotal = 0
            lumiEventsTotal = 0
            for streamer in lumiStreamerList:
                lumiEventsTotal += streamer['events']
                lumiSizeTotal += streamer['filesize']

            # check if we are over the max allowed rate
            if lumiEventsTotal > self.maxInputRate:
                self.markFailed(lumiStreamerList)
                continue

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

                        if newEventsTotal <= self.maxInputEvents:
                            eventsTotal = newEventsTotal
                            sizeTotal = newSizeTotal
                            streamerList.append(streamer)

                self.createJob(streamerList, eventsTotal, sizeTotal, timePerEvent, sizePerEvent, memoryRequirement)

                for streamer in streamerList:
                    lumiStreamerList.remove(streamer)

                createdJobs += 1

            if createdJobs > 1:
                splitLumis.append( { 'SUB' : self.subscription["id"],
                                     'LUMI' : lumi, 'NFILES' : nFiles } )

        if len(splitLumis) > 0:
            self.insertSplitLumisDAO.execute(binds = splitLumis)

        return


    def createJob(self, streamerList, jobEvents, jobSize, timePerEvent, sizePerEvent, memoryRequirement):
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
            f = File(id = streamer['id'],
                     lfn = streamer['lfn'])
            f.setLocation(streamer['location'], immediateSave = False)
            self.currentJob.addFile(f)

        # job time based on
        #   - 5 min initialization (twice)
        #   - 0.5MB/s repack speed
        #   - reco with timePerEvent
        #   - checksum calculation at 5MB/s
        #   - stageout at 5MB/s
        # job disk based on
        #   - streamer or RAW on local disk (factor 1)
        #   - FEVT/ALCARECO/DQM on local disk (sizePerEvent)
        jobTime = 600 + jobSize/500000 + jobEvents*timePerEvent + (jobEvents*sizePerEvent*2)/5000000
        self.currentJob.addResourceEstimates(jobTime = min(jobTime, 47*3600),
                                             disk = min(jobSize/1024 + jobEvents*sizePerEvent, 20000000),
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
