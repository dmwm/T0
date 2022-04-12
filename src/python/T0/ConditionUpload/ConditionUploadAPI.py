"""
_ConditionUploadAPI_

API for anyting related to PCL condition upload

"""
import os
import stat
import time
import shutil
import tarfile
import logging
import threading
import subprocess

from T0.ConditionUpload import upload

from WMCore.DAOFactory import DAOFactory


def uploadConditions(username, password, serviceProxy):
    """
    _uploadConditions_

    Called by Tier0Feeder in every polling cycle

    Determine PCL status incl. files for upload for all
    run/stream combos that are not finished yet.

    Loop through the runs, uploading files for all
    streams. If the run/stream  upload subscription
    is finished, mark that run/stream PCL as finished.

    Terminate the loop on the first run that has
    not completely finished streams, but only
    within a certain timeout based on the runs
    end time (either from the EoR record or based
    on the insertion time of the last streamer file).

    """
    logging.debug("uploadConditions()")
    myThread = threading.currentThread()

    daoFactory = DAOFactory(package = "T0.WMBS",
                            logger = logging,
                            dbinterface = myThread.dbi)

    getConditionsDAO = daoFactory(classname = "ConditionUpload.GetConditions")
    completeFilesDAO = daoFactory(classname = "ConditionUpload.CompleteFiles")

    finishPCLforEmptyExpressDAO = daoFactory(classname = "ConditionUpload.FinishPCLforEmptyExpress")

    isPromptCalibrationFinishedDAO = daoFactory(classname = "ConditionUpload.IsPromptCalibrationFinished")
    markPromptCalibrationFinishedDAO = daoFactory(classname = "ConditionUpload.MarkPromptCalibrationFinished")

    # look at all runs which are finished with conditions uploads
    # check for late arriving payloads and upload them
    conditions = getConditionsDAO.execute(finished = True, transaction = False)

    for (index, run) in enumerate(sorted(conditions.keys()), 1):

        dropboxHost = conditions[run]['dropboxHost']
        validationMode = conditions[run]['validationMode']

        for streamid, uploadableFiles in list(conditions[run]['streams'].items()):

            if len(uploadableFiles) > 0:

                uploadedFiles = uploadToDropbox(uploadableFiles, dropboxHost, validationMode,
                                                username, password, serviceProxy)

                if len(uploadedFiles) > 0:

                    bindVarList = []
                    for uploadedFile in uploadedFiles:
                        bindVarList.append( { 'FILEID' : uploadedFile['fileid'],
                                              'SUBSCRIPTION' : uploadedFile['subscription'] } )

                    # need a transaction here so we don't have files in
                    # state acquired and complete at the same time
                    try:
                        myThread.transaction.begin()
                        completeFilesDAO.execute(bindVarList, conn = myThread.transaction.conn, transaction = True)
                    except:
                        myThread.transaction.rollback()
                        raise
                    else:
                        myThread.transaction.commit()


    # check for pathological runs with no express data that will never
    # create conditions for upload and set them to finished
    finishPCLforEmptyExpressDAO.execute(transaction = False)

    # look at all runs not completely finished with condition uploads
    # return acquired (to be uploaded) files for them 
    conditions = getConditionsDAO.execute(finished = False, transaction = False)

    for (index, run) in enumerate(sorted(conditions.keys()), 1):

        advanceToNextRun = True

        timeout = conditions[run]['condUploadTimeout']
        dropboxHost = conditions[run]['dropboxHost']
        validationMode = conditions[run]['validationMode']

        for streamid, uploadableFiles in list(conditions[run]['streams'].items()):

            if len(uploadableFiles) > 0:

                uploadedFiles = uploadToDropbox(uploadableFiles, dropboxHost, validationMode,
                                                username, password, serviceProxy)

                if len(uploadedFiles) > 0:

                    bindVarList = []
                    for uploadedFile in uploadedFiles:
                        bindVarList.append( { 'FILEID' : uploadedFile['fileid'],
                                              'SUBSCRIPTION' : uploadedFile['subscription'] } )

                    # need a transaction here so we don't have files in
                    # state acquired and complete at the same time
                    try:
                        myThread.transaction.begin()
                        completeFilesDAO.execute(bindVarList, conn = myThread.transaction.conn, transaction = True)
                    except:
                        myThread.transaction.rollback()
                        raise
                    else:
                        myThread.transaction.commit()

                    # check if all files for run/stream uploaded (that means only complete
                    # files for same number of subscriptions as number of producers)
                    markPromptCalibrationFinishedDAO.execute(run, streamid, transaction = False)

                else:
                    # upload failed
                    advanceToNextRun = False

            else:
                # no files available for upload yet
                advanceToNextRun = False

        # check if all streams for run finished
        if advanceToNextRun:
            finished = isPromptCalibrationFinishedDAO.execute(run, transaction = False)
            if not finished:
                advanceToNextRun = False

        # check for timeout, but only if there is a next run
        if not advanceToNextRun and index < len(list(conditions.keys())):

            getRunStopTimeDAO = daoFactory(classname = "ConditionUpload.GetRunStopTime")
            stopTime = getRunStopTimeDAO.execute(run, transaction = False)

            if time.time() < stopTime + timeout:
                break

    return

def uploadToDropbox(condFiles, dropboxHost, validationMode,
                    username, password, serviceProxy):
    """
    _uploadToDropbox_

    Upload a number of files to the Dropbox

    The files are on AFS and are both sqlite and metadata.
    They also contain both the regular destination and the
    validation destionation, depending on the value of the
    passed in validationMode parameter one needs to be
    filtered out.

    """
    # sort files
    completeFiles = []
    filesDict = {}
    for condFile in condFiles:
        if condFile['lfn'] == "/no/output":
            completeFiles.append(condFile)
        else:
            (filenamePrefix, filenameExt) = os.path.basename(condFile['lfn']).split('.')
            if filenamePrefix not in filesDict:
                filesDict[filenamePrefix] = {}
            filesDict[filenamePrefix][filenameExt] = condFile

    for filenamePrefix in list(filesDict.keys()):

        sqliteFile = filesDict[filenamePrefix]['db']
        metaFile = filesDict[filenamePrefix]['txt']

        completeFiles.extend( uploadPayload(filenamePrefix, sqliteFile, metaFile,
                                            dropboxHost, validationMode,
                                            username, password,
                                            serviceProxy) )

    return completeFiles

def uploadPayload(filenamePrefix, sqliteFile, metaFile, dropboxHost, validationMode, username, password, serviceProxy):
    """
    _uploadPayload_

    Upload a single payload consisting of a sqlite
    file and a metadata file to the dropbox.
    
    """
    completeFiles = []
    files2delete = []
    inputCopied = True

    filenameDB = filenamePrefix + ".db"
    filenameTXT = filenamePrefix + ".txt"
    filenameTAR = filenamePrefix + ".tar.bz2"

    eosPrefix = "root://eoscms.cern.ch//eos/cms"
    sqliteFile['pfn'] = eosPrefix + sqliteFile['lfn']
    metaFile['pfn'] = eosPrefix + metaFile['lfn']

    command = "export X509_USER_PROXY=%s\n" % serviceProxy
    command += "env KRB5CCNAME=/tmp/bla xrdcp -s -f %s %s" % (sqliteFile['pfn'], filenameDB)
    p = subprocess.Popen(command, shell = True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    output = p.communicate()[0].decode('utf-8')
    if p.returncode > 0:
        logging.error("Failure during copy from EOS: %s" % output)
        logging.error("  ==> Upload failed for payload %s" % filenamePrefix)
        inputCopied = False
    else:
        files2delete.append(filenameDB)

    command = "export X509_USER_PROXY=%s\n" % serviceProxy
    command += "env KRB5CCNAME=/tmp/bla xrdcp -s -f %s %s" % (metaFile['pfn'], filenameTXT)
    p = subprocess.Popen(command, shell = True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    output = p.communicate()[0].decode('utf-8')
    if p.returncode > 0:
        logging.error("Failure during copy from EOS: %s" % output)
        logging.error("  ==> Upload failed for payload %s" % filenamePrefix)
        inputCopied = False
    else:
        files2delete.append(filenameTXT)

    # select the right destination db depending
    # on whether we are in validation mode
    if inputCopied:
        with open(filenameTXT) as fin:
            lines = fin.readlines()
            fin.close()
        with open(filenameTXT, 'w') as fout:
            if validationMode:
                fout.writelines( [ line.replace('prepMetaData ', '', 1) for line in lines if 'prodMetaData ' not in line] )
            else:
                fout.writelines( [ line.replace('prodMetaData ', '', 1) for line in lines if 'prepMetaData ' not in line] )
            fout.close()

        os.chmod(filenameDB, stat.S_IREAD | stat.S_IWRITE | stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)
        os.chmod(filenameTXT, stat.S_IREAD | stat.S_IWRITE | stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)

        if username == None or password == None:
            completeFiles.append(sqliteFile)
            completeFiles.append(metaFile)
            logging.info("No username/password provided for DropBox upload...")
            logging.info("  ==> Upload skipped for payload %s" % filenamePrefix)
        elif serviceProxy == None:
            completeFiles.append(sqliteFile)
            completeFiles.append(metaFile)
            logging.info("No service proxy provided to access EOS for uploaded record...")
            logging.info("  ==> Upload skipped for payload %s" % filenamePrefix)
        else:
            # needed by the PCL monitoring to know whether we uploaded to prod or validation
            command = "export X509_USER_PROXY=%s\n" % serviceProxy
            command += "env KRB5CCNAME=/tmp/bla XRD_WRITERECOVERY=0 xrdcp -s -f %s %s" % (filenameTXT, metaFile['pfn'] + ".uploaded")
            p = subprocess.Popen(command, shell = True,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
            output = p.communicate()[0].decode('utf-8')
            if p.returncode > 0:
                logging.error("Failure during copy of .uploaded file to EOS: %s" % output)
                logging.error("  ==> Upload failed for payload %s" % filenamePrefix)
            else:
                uploadStatus = True
                try:
                    upload.uploadTier0Files([filenameDB], username, password)
                except:
                    # Remove the re-raising of the exception if you want to resume operations while fixing the issue
                    raise RuntimeError("Unable to upload T0 files to Dropbox...")
                    logging.exception("Something went wrong with the Dropbox upload...")
                    uploadStatus = False

                if uploadStatus:
                    completeFiles.append(sqliteFile)
                    completeFiles.append(metaFile)
                    logging.info("  ==> Upload succeeded for payload %s" % filenamePrefix)
                else:
                    logging.error("  ==> Upload failed for payload %s" % filenamePrefix)

    for file2delete in files2delete:
        os.remove(file2delete)

    return completeFiles
