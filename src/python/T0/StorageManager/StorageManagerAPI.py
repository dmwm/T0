"""
_StorageManagerAPI_

Contains all the code for interfacing with the StorageManager

"""
import logging
import threading
import time

from WMCore.DAOFactory import DAOFactory

knownStreamers = set()

def injectNewData(dbInterfaceStorageManager,
                  dbInterfaceHltConf,
                  dbInterfaceSMNotify,
                  streamerPNN,
                  minRun = None,
                  maxRun = None,
                  injectRun = None):
    """
    _injectNewData_

    Replaces the old-style file notification injecton into the Tier0.

    Queries the StorageManager database for new data and injects it into the Tier0.

    These queries will find duplicates, ie. data that was already found and
    processed in a previous polling cycle. Code has to be robust against that.

    Needs to be passed the PNN on which streamer files are located

    """
    logging.debug("injectNewData()")
    myThread = threading.currentThread()

    daoFactory = DAOFactory(package = "T0.WMBS",
                            logger = logging,
                            dbinterface = myThread.dbi)

    daoFactoryStorageManager = DAOFactory(package = "T0.WMBS",
                                          logger = logging,
                                          dbinterface = dbInterfaceStorageManager)

    daoFactoryHltConf = DAOFactory(package = "T0.WMBS",
                                   logger = logging,
                                   dbinterface = dbInterfaceHltConf)

    if dbInterfaceSMNotify:
        daoFactorySMNotify = DAOFactory(package = "T0.WMBS",
                                        logger = logging,
                                        dbinterface = dbInterfaceSMNotify)
        insertFileStatusDAO = daoFactorySMNotify(classname = "SMNotification.InsertOfflineFileStatus")

    getNewDataDAO = daoFactoryStorageManager(classname = "StorageManager.GetNewData")
    getRunInfoDAO = daoFactoryHltConf(classname = "StorageManager.GetRunInfo")
    insertRunDAO = daoFactory(classname = "RunConfig.InsertRun")
    insertStreamDAO = daoFactory(classname = "RunConfig.InsertStream")
    insertCMSSWVersionDAO = daoFactory(classname = "RunConfig.InsertCMSSWVersion")
    insertStreamCMSSWVersionDAO = daoFactory(classname = "RunConfig.InsertStreamCMSSWVersion")
    insertLumiDAO = daoFactory(classname = "RunConfig.InsertLumiSection")
    insertStreamerDAO = daoFactory(classname = "RunConfig.InsertStreamer")

    newData = getNewDataDAO.execute(minRun = minRun,
                                    maxRun = maxRun,
                                    injectRun = injectRun, 
                                    transaction = False)

    # remove already processed files
    newData[:] = [newFile for newFile in newData if newFile['p5_id'] not in knownStreamers]

    logging.debug("StoragemanagerAPI: found %d new files", len(newData))

    newRuns = set()
    newRunStreams = {}
    for newFile in newData:

        run = newFile['run']
        stream = newFile['stream']

        newRuns.add(newFile['run'])

        if run not in newRunStreams:
            newRunStreams[run] = set()
        if stream not in newRunStreams[run]:
            newRunStreams[run].add(stream)

    logging.debug("StoragemanagerAPI: found %d new runs", len(newRuns))

    cmsswVersions = set()
    streams = set()
    bindRunHltKey = []
    bindRunStreamCMSSW = []
    for run in sorted(list(newRuns)):
        (hltkey, cmssw) = getRunInfoDAO.execute(run = run, transaction = False)
        logging.debug("StorageManagerAPI: run = %d, hltkey = %s, cmssw = %s", run, hltkey, cmssw)
        if hltkey and cmssw:
            cmssw = '_'.join(cmssw.split('_')[0:4]) # only consider base release
            cmsswVersions.add(cmssw)
            bindRunHltKey.append( { 'RUN': run,
                                    'HLTKEY': hltkey } )
            for stream in newRunStreams[run]:
                streams.add(stream)
                bindRunStreamCMSSW.append( { 'RUN': run,
                                             'STREAM': stream,
                                             'VERSION': cmssw } )
        else:
            # can't retrieve hltkey and cmssw for run, ignore any data for it
            newRuns.remove(run)

    if len(bindRunHltKey) > 0:
        insertRunDAO.execute(binds = bindRunHltKey, transaction = False)

    bindStream = []
    for stream in streams:
        bindStream.append( { 'STREAM': stream } )
    if len(bindStream) > 0:
        insertStreamDAO.execute(binds = bindStream, transaction = False)

    bindCMSSW = []
    for cmssw in cmsswVersions:
        bindCMSSW.append( { 'VERSION': cmssw } )
    if len(bindCMSSW) > 0:
        insertCMSSWVersionDAO.execute(binds = bindCMSSW, transaction = False)

    if len(bindRunStreamCMSSW) > 0:
        insertStreamCMSSWVersionDAO.execute(binds = bindRunStreamCMSSW, transaction = False)

    lumis = set()
    bindStreamer = []
    bindInsertFileStatus = []
    for newFile in newData:

        run = newFile['run']

        if run not in newRuns:
            continue

        lumi = newFile['lumi']
        lumis.add((run,lumi))

        if newFile['filename'] == 'run289461_ls0020_streamExpressCosmics_StorageManager.dat':
            newFile['path'] = '/store/t0streamer/Data/ExpressCosmics/000/289/461'

        bindStreamer.append( { 'LFN': newFile['path'] + '/' + newFile['filename'],
                               'P5_ID': newFile['p5_id'],
                               'RUN': run,
                               'LUMI': lumi,
                               'STREAM': newFile['stream'],
                               'FILESIZE': newFile['filesize'],
                               'EVENTS': newFile['events'],
                               'TIME': int(time.time()) } )

        if dbInterfaceSMNotify:
            bindInsertFileStatus.append( { 'P5_ID': newFile['p5_id'],
                                           'FILENAME': newFile['filename'] } )

    bindLumi = []
    for lumi in lumis:
        bindLumi.append( { 'RUN': lumi[0],
                           'LUMI': lumi[1] } )
    if len(bindLumi) > 0:
        insertLumiDAO.execute(binds = bindLumi, transaction = False)

    if len(bindStreamer) > 0:
        insertStreamerDAO.execute(streamerPNN, binds = bindStreamer, transaction = False)

    if len(bindInsertFileStatus) > 0:
        insertFileStatusDAO.execute(bindInsertFileStatus, transaction = False)

    for x in bindStreamer:
        knownStreamers.add(x['P5_ID'])

    return

def markRepacked(dbInterfaceSMNotify):
    """
    _markRepacked_

    Find all finished streamers for closed all run/stream
    Update the StorageManager notification table
    Update the streamer status to finished (deleted = 1)

    """
    if not dbInterfaceSMNotify:
        return

    logging.debug("updateFileStatus()")
    myThread = threading.currentThread()

    daoFactory = DAOFactory(package = "T0.WMBS",
                            logger = logging,
                            dbinterface = myThread.dbi)

    daoFactorySMNotify = DAOFactory(package = "T0.WMBS",
                                    logger = logging,
                                    dbinterface = dbInterfaceSMNotify)

    getFinishedStreamersDAO = daoFactory(classname = "SMNotification.GetFinishedStreamers")
    updateFileStatusDAO = daoFactorySMNotify(classname = "SMNotification.UpdateOfflineFileStatus")
    markStreamersFinishedDAO = daoFactory(classname = "SMNotification.MarkStreamersFinished")

    finishedStreamers = getFinishedStreamersDAO.execute(transaction = False)

    streamers = []
    bindUpdateFileStatus = []
    for (streamer_id, p5_id) in finishedStreamers:
        streamers.append(streamer_id)
        bindUpdateFileStatus.append( { 'P5_ID': p5_id } )

    if len(bindUpdateFileStatus) > 0:
        updateFileStatusDAO.execute(bindUpdateFileStatus, transaction = False)

    if len(streamers) > 0:
        markStreamersFinishedDAO.execute(streamers, transaction = False)

    return
