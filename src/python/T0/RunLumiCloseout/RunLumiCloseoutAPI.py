"""
_RunLumiCloseoutAPI_

API for anyting RunConfig related

"""
import logging
import threading
import time

from WMCore.DAOFactory import DAOFactory


def stopRuns(dbInterfaceStorageManager):
    """
    _stopRuns_

    Called by Tier0Feeder

    For all active runs check the RunSummary records to see if the
    run has stoppedended. If it has, update T0AST to reflect this.

    Replays are handled differently, they will update start_time and
    stop_time with the min and max streamer insert times.

    """
    logging.debug("stopRuns()")
    myThread = threading.currentThread()
    
    daoFactory = DAOFactory(package = "T0.WMBS",
                            logger = logging,
                            dbinterface = myThread.dbi)

    daoFactoryStorageManager = DAOFactory(package = "T0.WMBS",
                                          logger = logging,
                                          dbinterface = dbInterfaceStorageManager)

    findActiveRunsDAO = daoFactory(classname = "RunLumiCloseout.FindActiveRuns")
    findStoppedRunsDAO = daoFactoryStorageManager(classname = "RunLumiCloseout.FindStoppedRuns")
    stopRunsDAO = daoFactory(classname = "RunLumiCloseout.StopRuns")

    # find all active runs
    #
    # for replays this does all the work of checking close_time
    # and setting stop_time to the same (skipped the other checks)
    activeRuns = findActiveRunsDAO.execute(transaction = False)

    # then check which one of them have ended
    if len(activeRuns) > 0:

        stoppedRuns = findStoppedRunsDAO.execute(runs = activeRuns, transaction = False)

        bindVarList = []
        for run, (start_time, stop_time) in list(stoppedRuns.items()):
            bindVarList.append( { 'RUN' : run,
                                  'START_TIME' : start_time,
                                  'STOP_TIME' : stop_time } )

        # and mark them as stopped in T0AST
        if len(bindVarList) > 0:
            stopRunsDAO.execute(binds = bindVarList, transaction = False)

    return


def closeRuns(dbInterfaceStorageManager):
    """
    _closeRuns_

    Called by Tier0Feeder

    For all open runs check the StorageManager EoR records to see if the run has ended.
    If it has, update T0AST to reflect this.

    For all runs with open run/stream filesets recheck the StorageManager EoR records
    to see if the lumicount has changed. Update T0AST if it has.

    """
    logging.debug("closeRuns()")
    myThread = threading.currentThread()

    daoFactory = DAOFactory(package = "T0.WMBS",
                            logger = logging,
                            dbinterface = myThread.dbi)

    daoFactoryStorageManager = DAOFactory(package = "T0.WMBS",
                                          logger = logging,
                                          dbinterface = dbInterfaceStorageManager)

    findOpenRunsDAO = daoFactory(classname = "RunLumiCloseout.FindOpenRuns")
    findClosedRunsDAO = daoFactoryStorageManager(classname = "RunLumiCloseout.FindClosedRuns")
    closeRunsDAO = daoFactory(classname = "RunLumiCloseout.CloseRuns")
    getOpenRunStreamLumicountDAO = daoFactory(classname = "RunLumiCloseout.GetOpenRunStreamLumicount")

    # find all open runs and check which ones have ended
    openRuns = findOpenRunsDAO.execute(transaction = False)
    if len(openRuns) > 0:
        closedRuns = findClosedRunsDAO.execute(runs = openRuns, transaction = False)
    else:
        closedRuns = {}

    # find all runs with open run/stream filesets and check which have changed lumicount, update those
    runLumicountT0 = getOpenRunStreamLumicountDAO.execute(transaction = False)
    if len(runLumicountT0) > 0:
        runLumicountSM = findClosedRunsDAO.execute(runs = list(runLumicountT0.keys()), transaction = False)
        for run, lumicount in list(runLumicountSM.items()):
            if lumicount != runLumicountT0[run]:
                closedRuns[run] = lumicount

    if len(closedRuns) > 0:
        bindVarList = []
        currentTime = int(time.time())
        for run, lumicount in list(closedRuns.items()):
            bindVarList.append( { 'RUN' : run,
                                  'LUMICOUNT' : lumicount,
                                  'CLOSE_TIME' : currentTime } )

        # mark run as closed and update lumicount
        if len(bindVarList) > 0:
            closeRunsDAO.execute(binds = bindVarList, transaction = False)

    return


def closeLumiSections(dbInterfaceStorageManager):
    """
    _closeLumiSections_

    Called by Tier0Feeder

    For each active run:stream (where corresponding fileset
    exists and is open), find new lumis in StorageManager
    database and create matching lumi_section_closed records

    Also check for all not finally closed lumis if the number
    of streamers matches the filecount in the lumi_section_closed
    record and final close them if it does

    """
    logging.debug("closeLumiSections()")
    myThread = threading.currentThread()

    daoFactory = DAOFactory(package = "T0.WMBS",
                            logger = logging,
                            dbinterface = myThread.dbi)

    daoFactoryStorageManager = DAOFactory(package = "T0.WMBS",
                                          logger = logging,
                                          dbinterface = dbInterfaceStorageManager)

    findHighContLumiDAO = daoFactory(classname = "RunLumiCloseout.FindHighContLumi")
    findClosedLumisDAO = daoFactoryStorageManager(classname = "RunLumiCloseout.FindClosedLumis")
    insertLumiDAO = daoFactory(classname = "RunConfig.InsertLumiSection")
    insertClosedLumiDAO = daoFactory(classname = "RunLumiCloseout.InsertClosedLumi")
    finalCloseLumiDAO = daoFactory(classname = "RunLumiCloseout.FinalCloseLumi")

    currentTime = int(time.time())

    # find active run/streams and their highest lumi
    # in a continious 1...lumi sequence
    runStreamLumis = findHighContLumiDAO.execute(transaction = False)

    # nothing active, nothing to do
    if len(runStreamLumis) == 0:
        return

    # find new closed lumis based on EoLS records for
    # any given run/stream and lumi > N 
    closedLumis = findClosedLumisDAO.execute(binds = runStreamLumis, transaction = False)

    if len(closedLumis) > 0:

        #
        # insert all lumis we find, but have to take care of duplicates
        # (due to having the same lumi for different streams)
        #
        runLumis = {}
        for closedLumi in closedLumis:
            run = closedLumi['RUN']
            lumi = closedLumi['LUMI']
            if run not in runLumis:
                runLumis[run] = set()
            runLumis[run].add(lumi)

        bindVarList = []
        for run, lumis in list(runLumis.items()):
            for lumi in lumis:
                bindVarList.append( { 'RUN' : run,
                                      'LUMI' : lumi } )

        insertLumiDAO.execute(binds = bindVarList,
                              transaction = False)

        for closedLumi in closedLumis:
            closedLumi['INSERT_TIME'] = currentTime
            if closedLumi['FILECOUNT'] == 0:
                closedLumi['CLOSE_TIME'] = currentTime
            else:
                closedLumi['CLOSE_TIME'] = 0

        # insert closed lumis record
        insertClosedLumiDAO.execute(binds = closedLumis, transaction = False)

    # final lumi closing
    finalCloseLumiDAO.execute(currentTime, transaction = False)

    return


def closeRunStreamFilesets():
    """
    _closeRunStreamFilesets_

    Called by Tier0Feeder

    For active run/stream (fileset open) and ended run
    with all lumis between 1 to high lumi present and
    final closed and all streamers feed, we are sure to
    have all the data there is. Close the run/stream
    fileset to start processing closeout.

    This is all done in a single query.

    """
    logging.debug("closeRunStreamFilesets()")
    myThread = threading.currentThread()

    daoFactory = DAOFactory(package = "T0.WMBS",
                            logger = logging,
                            dbinterface = myThread.dbi)

    closeRunStreamFilesetsDAO = daoFactory(classname = "RunLumiCloseout.CloseRunStreamFilesets")

    closeRunStreamFilesetsDAO.execute(transaction = False)

    return


def checkActiveSplitLumis():
    """
    _checkActiveSplitLumis_

    Called by Tier0Feeder

    For active split lumis, check if all streamers in
    the run/lumi/stream have been fully processed, ie.
    none of the streamers are available, acquired or
    failed. If this is the case, delete the split lumi.

    This is all done in a single query.

    """
    logging.debug("checkActiveSplitLumi()")
    myThread = threading.currentThread()

    daoFactory = DAOFactory(package = "T0.WMBS",
                            logger = logging,
                            dbinterface = myThread.dbi)

    checkActiveSplitLumisDAO = daoFactory(classname = "RunLumiCloseout.CheckActiveSplitLumis")

    checkActiveSplitLumisDAO.execute(transaction = False)

    return
