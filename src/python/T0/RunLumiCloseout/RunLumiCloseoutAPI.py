"""
_RunLumiCloseoutAPI_

API for anyting RunConfig related

"""
import logging
import threading
import time

from WMCore.DAOFactory import DAOFactory


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

    bindVarList = []
    for closedLumi in closedLumis:
        bindVarList.append( { 'RUN' : closedLumi['RUN'],
                              'LUMI' : closedLumi['LUMI'] } )
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
