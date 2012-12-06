#!/usr/bin/env python
"""
__DiagnoseActiveRuns__

Check a given run and look
for problems in the input streamer data,
e.g. incomplete data for lumis, EoLS/EoR missing records
"""

import logging
import os
import re
import sys
import traceback

from optparse import OptionParser

from T0 import version as T0Version
from WMCore.Configuration import loadConfigurationFile
from WMCore.DAOFactory import DAOFactory
from WMCore.Database.DBFactory import DBFactory
from WMCore.Database.Transaction import Transaction
from WMCore.Services.WMStats.WMStatsReader import WMStatsReader

def buildLumiRanges(lumiList):
    """
    _buildLumiRanges_

    Get a list of integer
    lumi ids and build a list
    of tuples with the lumis in closed ranges
    """
    lumiRanges = []
    firstLumi = lumiList[0]
    lastLumi = lumiList[0]
    for singleLumi in lumiList[1:]:
        if singleLumi != lastLumi + 1:
            lumiRanges.append((firstLumi, lastLumi))
            firstLumi = singleLumi
        lastLumi = singleLumi
    lumiRanges.append((firstLumi, lastLumi))
    return lumiRanges

def diagnoseRun(runNumber, doChange):
    """
    _diagnoseRun_

    Gets a run number and checks if it is active
    and why. Particularly looks for problems in the input
    lumi sections from SM.
    """
    # Setup everything, first the configuration
    if "WMAGENT_CONFIG" not in os.environ:
        logging.error("WMAGENT_CONFIG is not in the environment. Exiting.")
        return 1

    wmat0Config = loadConfigurationFile(os.environ["WMAGENT_CONFIG"])
    t0astConnectUrl = wmat0Config.CoreDatabase.connectUrl
    storageManagerConnectUrl = wmat0Config.StorageManagerDatabase.connectUrl

    # Get all the DAO factories and DB interfaces
    dbFactoryT0AST = DBFactory(logging, dburl = t0astConnectUrl, options = {})
    dbInterfaceT0AST = dbFactoryT0AST.connect()
    daoFactoryT0AST = DAOFactory(package = "T0.WMBS",
                                 logger = logging,
                                 dbinterface = dbInterfaceT0AST)
    daoFactoryWMBS = DAOFactory(package = "WMCore.WMBS",
                                logger = logging,
                                dbinterface = dbInterfaceT0AST)

    dbFactorySM = DBFactory(logging, dburl = storageManagerConnectUrl, options = {})
    dbInterfaceSM = dbFactorySM.connect()
    daoFactorySM = DAOFactory(package = "T0.WMBS",
                                 logger = logging,
                                 dbinterface = dbInterfaceSM)

    # It needs WMStats as well
    localWmstatsUrl = wmat0Config.AnalyticsDataCollector.localWMStatsURL
    localDBreader = WMStatsReader(localWmstatsUrl)

    # Start the checks
    findActiveRunsDAO = daoFactoryT0AST(classname = "RunLumiCloseout.FindActiveRuns")
    activeRuns = findActiveRunsDAO.execute()

    if int(runNumber) in activeRuns:
        logging.debug("Run has not ended yet, checking EoR records...")
        # Run has not ended yet, check if it's an issue with EoR records
        checkEoRRecordsDAO = daoFactorySM(classname = "RunLumiCloseout.CheckEndOfRunRecords")
        result = checkEoRRecordsDAO.execute(run = runNumber)
        if result["totalInstances"] != (len(result["instancesWithEoR"]) + len(result["instancesWithoutEoR"])):
            logging.error("Number of instances in SM don't match.")
        if result["instancesWithEoR"] and result["instancesWithoutEoR"]:
            for instance in result["instancesWithoutEoR"]:
                print "Instance %s didn't write an EoR record." % instance
        elif result["instancesWithEoR"]:
            print "Run %s has already ended according to SM, but not in T0AST. Check the Tier0Feeder" % runNumber
        else:
            print "Run %s has not ended yet according to SM." % runNumber
        return 0

    findEndedRunsDAO = daoFactorySM(classname = "RunLumiCloseout.FindEndedRuns")
    endedRuns = findEndedRunsDAO.execute([runNumber])

    if not endedRuns:
        logging.error("Run does not exist. Exiting.")
        return 1

    logging.debug("Run has already ended, checking WMStats to see if it is closed.")

    activeWorkflows = localDBreader.workflowsByStatus(["new"], stale = False)
    closedWorkflows = localDBreader.workflowsByStatus([], stale = False)
    regex = re.compile(r"^[\w]+_Run%s_[\w]+$" % runNumber)
    matchingWorkflows = filter(regex.match, activeWorkflows)
    matchingAllWorkflows = filter(regex.match, closedWorkflows)

    if not matchingWorkflows and not matchingAllWorkflows:
        print "Run is not yet available in WMStats."
        return 0
    elif not matchingWorkflows:
        print "All workflows associated to the run are closed already."
        return 0

    for workflow in matchingWorkflows:
        logging.debug("%s is still not closed" % workflow)

    logging.debug("Checking for missing EoLS records")

    lumiCloseDAO = daoFactoryT0AST(classname = "RunLumiCloseout.CheckClosedLumis")
    closedRecords = lumiCloseDAO.execute(run = runNumber)

    affectedStreams = {}

    for entry in closedRecords:
        if entry["closed_lumi_count"] != entry["expected_lumi_count"] or \
           entry["closed_lumi_count"] != entry["max_lumi"]:
            affectedStreams[entry["stream_id"]] = range(1, entry["expected_lumi_count"] + 1)

    # If there are lumis with mismatching EoLS, report on the specific lumis
    if affectedStreams:
        print "There are missing EoLS records"
        logging.debug("Checking individual streams")
        closedLumisDAO = daoFactoryT0AST(classname = "RunLumiCloseout.GetClosedLumisForStream")
        closedLumis = closedLumisDAO.execute(run = runNumber, streams = affectedStreams.keys())

        for stream in affectedStreams:
            logging.debug("Stream %s has lumis missing EoLS" % stream)
            lumiList = affectedStreams[stream]
            closedLumiList = closedLumis[stream]["closedLumis"]
            openLumis = set(lumiList) - set(closedLumiList)
            spuriousLumis = set(closedLumiList) - set(lumiList)

            # Missing EoLS found
            if openLumis:
                lumis = sorted(list(openLumis))
                lumiRanges = buildLumiRanges(lumis)
                msg = "Stream %s has missing EoLS records in lumis: %s" % (closedLumis[stream]["name"],
                                                                                    str(sorted(lumiRanges)))
                print msg

            # Extra closed lumi section records found
            if spuriousLumis:
                lumis = sorted(list(spuriousLumis))
                lumiRanges = buildLumiRanges(lumis)
                msg = "Stream %s has spurious EoLS records in lumis: %s" % (closedLumis[stream]["name"],
                                                                                     str(sorted(lumiRanges)))
                print msg
        return 0

    logging.debug("There are no EoLS missing records")
    logging.debug("Checking for incomplete data in lumis")

    openLumisDAO = daoFactoryT0AST(classname = "RunLumiCloseout.GetFileCountOnOpenLumis")
    openLumis = openLumisDAO.execute(run = runNumber)

    # Not problem so far, point the user to other systems.
    if not openLumis:
        print "No problem was found, check WMStats monitoring if run is still marked as Active."
        return 0

    # Inform about the lumis with missing/extra streamers
    for streamKey in openLumis:
        print "Stream %s has lumis with inconsistent data" % streamKey[1]
        for lumi in openLumis[streamKey]:
            msg = "Lumi %s has a mismatching number of streamers:\n Expected: %s, Found: %s" % (lumi, openLumis[streamKey][lumi][0], openLumis[streamKey][lumi][1])
            print msg

    if doChange:
        # We are changing T0AST to closeout the run
        logging.info("Making changes to T0AST, wiping incomplete lumis.")

        # Get the files to delete
        filesForStreamDAO = daoFactoryT0AST(classname = "RunLumiCloseout.GetFilesForStreamLumi")
        streams = dict((streamKey[0], openLumis[streamKey]) for streamKey in openLumis)
        fileList = filesForStreamDAO.execute(runNumber, streams)

        # Log the full extent of the action
        logging.info("Inserting into lumi_section_closed:")
        for stream in streams:
            for lumi in streams[stream]:
                logging.info("    Run: %s, Stream: %s, Lumi: %s" % (runNumber, stream, lumi))
        if fileList:
            logging.info("Removing from STREAMER and WMBS_FILE_DETAILS")
        for fileId in fileList:
            logging.info(" ID: %s, LFN: %s" % (fileId, fileList[fileId]))

        trans = None
        try:
            # Wrap it in a transaction since it is a delicate operation
            trans = Transaction(dbinterface = dbInterfaceT0AST)
            trans.begin()

            # Close the lumis with 0 streamers
            forceCloseLumiDAO = daoFactoryT0AST(classname = "RunLumiCloseout.ForceCloseLumi")
            forceCloseLumiDAO.execute(runNumber, streams, conn = trans.conn, transaction = True)

            deleteStreamerDAO = daoFactoryT0AST(classname = "RunLumiCloseout.DeleteStreamers")
            deleteWMBSFileDAO = daoFactoryWMBS(classname = "Files.Delete")
            if fileList:
                # Get rid of the remaining streamer files
                deleteStreamerDAO.execute(fileList.keys(), conn = trans.conn, transaction = True)
                deleteWMBSFileDAO.execute(fileList.values(), conn = trans.conn, transaction = True)

            # Everything went well, commit it
            trans.commit()
            print "Done with the changes, run should close soon."
            return 0
        except Exception, ex:
            if trans:
                # In case of error, rollback and close connection
                trans.rollbackForError()
            logging.error("Failed to make changes:\n %s" % str(ex))
            logging.error(traceback.format_exc())

            return 1

    return 0

def main():
    """
    _main_

    Parse the options and check the requested run
    """
    usage = "Usage: %prog [options] RunNumber"
    version = "Compatible with: %s" % T0Version
    parser = OptionParser(usage = usage, version = version)
    parser.add_option("--wipe-incomplete-lumi", action = "store_true", default = False,
                      dest = "fixIncompleteLumi", help = "Wipes lumis with incomplete data from T0AST")
    parser.add_option("-v", "--verbose", action = "store_true", default = False,
                      dest = "verbose", help = "Prints DEBUG logging statements")
    parser.add_option("-s", "--silent", action = "store_true", default = False,
                      dest = "silent", help = "Suppress any logging statements below ERROR level")
    (options, args) = parser.parse_args()

    if options.verbose and options.silent:
        print "Conflicting options: silent and verbose. Exiting."
        return 1
    loggingLevel = logging.INFO
    if options.silent:
        loggingLevel = logging.ERROR
    if options.verbose:
        loggingLevel = logging.DEBUG
    logging.basicConfig(level = loggingLevel)
    logging.debug("Set verbose console output.")

    # Check the run number
    if not len(args):
        logging.error("No run number was provided. Exiting.")
        return 1
    runNumber = args[0]
    try:
        runNumber = int(runNumber)
    except:
        logging.error("Invalid wrong number. Exiting.")
        return 1

    return diagnoseRun(str(runNumber), options.fixIncompleteLumi)

if __name__ == '__main__':
    sys.exit(main())
