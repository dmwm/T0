"""
_Repack_

Splitting algorithm for repacking.
"""

import logging
import threading

from WMCore.WMBS.File import File

from WMCore.JobSplitting.JobFactory import JobFactory
from WMCore.DAOFactory import DAOFactory
from WMCore.Services.UUID import makeUUID


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

        self.createdGroup = False

        myThread = threading.currentThread()
        daoFactory = DAOFactory(package = "T0.WMBS",
                                logger = logging,
                                dbinterface = myThread.dbi)

        maxLumiWithJobDAO = daoFactory(classname = "Subscriptions.MaxLumiWithJob")
        getClosedEmptyLumisDAO = daoFactory(classname = "JobSplitting.GetClosedEmptyLumis")

        # keep for later
        self.insertSplitLumisDAO = daoFactory(classname = "JobSplitting.InsertSplitLumis")

        # data discovery
        getFilesDAO = daoFactory(classname = "Subscriptions.GetAvailableRepackFiles")
        availableFiles = getFilesDAO.execute(self.subscription["id"])

        # nothing to do, stop immediately
        if len(availableFiles) == 0:
            return

        # lumis we have data for
        lumiList = set([])
        for result in availableFiles:
            lumiList.add(result['lumi'])
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
        lumi = maxLumiWithJob + 1
        while lumi in lumiList:
            lumi += 1
        if lumi < lumiList[-1]:
            detectEmptyLumis = True

        # empty and closed lumis
        emptyLumis = []
        if detectEmptyLumis:
            emptyLumis = getClosedEmptyLumisDAO.execute(self.subscription["id"], maxLumiWithJob)

        # figure out lumi range to create jobs for
        streamersByLumi = {}
        firstLumi = maxLumiWithJob + 1
        lastLumi = lumiList[-1]
        for lumi in range(firstLumi, lastLumi + 1):
            if (lumi in lumiList) or (lumi in emptyLumis):
                streamersByLumi[lumi] = []
            else:
                break

        # figure out what data to create jobs for
        for fileInfo in availableFiles:
            lumi = fileInfo['lumi']
            if streamersByLumi.has_key(lumi):
                streamersByLumi[lumi].append(fileInfo)

        # check if fileset is closed
        fileset = self.subscription.getFileset()
        fileset.load()

        self.defineJobs(streamersByLumi, fileset.open)

        return


    def defineJobs(self, streamersByLumi, filesetOpen):
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

                splitLumis.append( { 'SUB' : self.subscription["id"],
                                     'LUMI' : lumi } )

                # repack what we have to preserve order
                if len(jobStreamerList) > 0:
                    self.createJob(jobStreamerList)
                    jobSizeTotal = 0
                    jobEventsTotal = 0
                    jobStreamerList = []

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

                    self.createJob(streamerList)

                    for streamer in streamerList:
                        lumiStreamerList.remove(streamer)

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

                    self.createJob(jobStreamerList)

                    jobSizeTotal = lumiSizeTotal
                    jobEventsTotal = lumiEventsTotal
                    jobStreamerList = lumiStreamerList

        # if we are in closeout issue repack job for leftovers
        if len(jobStreamerList) > 0 and not filesetOpen:
            self.createJob(jobStreamerList)

        if len(splitLumis) > 0:
            self.insertSplitLumisDAO.execute(binds = splitLumis)

        return


    def createJob(self, streamerList):
        """
        _createJob_

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
