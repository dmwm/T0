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


def uploadConditions(username, password):
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

    findConditionsDAO = daoFactory(classname = "ConditionUpload.GetConditions")
    completeFilesDAO = daoFactory(classname = "ConditionUpload.CompleteFiles")

    isPromptCalibrationFinishedDAO = daoFactory(classname = "ConditionUpload.IsPromptCalibrationFinished")
    markPromptCalibrationFinishedDAO = daoFactory(classname = "ConditionUpload.MarkPromptCalibrationFinished")

    # look at all runs not completely finished with condition uploads
    # return acquired (to be uploaded) files for them 
    conditions = findConditionsDAO.execute(transaction = False)

    now = time.time()

    for (index, run) in enumerate(sorted(conditions.keys()), 1):

        advanceToNextRun = True

        timeout = conditions[run]['condUploadTimeout']
        dropboxHost = conditions[run]['dropboxHost']
        validationMode = conditions[run]['validationMode']

        for streamid in conditions[run]['streams'].keys():

            subscription = conditions[run]['streams'][streamid]['subscription']

            # always upload files (if there are any to upload)
            condFiles = []
            uploadedFiles = []
            for condFile in conditions[run]['streams'][streamid]['files']:
                condFiles.append(condFile)
            if len(condFiles) > 0:
                uploadedFiles = uploadToDropbox(condFiles, dropboxHost, validationMode, username, password)

            bindVarList = []
            for uploadedFile in uploadedFiles:
                bindVarList.append( { 'FILEID' : uploadedFile['fileid'],
                                      'SUBSCRIPTION' : subscription } )

            # need a transaction here so we don't have files in
            # state acquired and complete at the same time
            if len(bindVarList) > 0:
                try:
                    myThread.transaction.begin()
                    completeFilesDAO.execute(bindVarList, transaction = True)
                except:
                    myThread.transaction.rollback()
                    raise
                else:
                    myThread.transaction.commit()

            # only finish and advance to next run if all run/stream finished
            # that means fileset for subscription closed and no available/acquired files
            if subscription != None:
                finished = isPromptCalibrationFinishedDAO.execute(subscription)
                if finished:
                    markPromptCalibrationFinishedDAO.execute(run, streamid, transaction = False)
                else:
                    advanceToNextRun = False
            else:
                advanceToNextRun = False

        # check for timeout, but only if there is a next run
        if not advanceToNextRun and index < len(conditions.keys()):

            getRunEndTimeDAO = daoFactory(classname = "ConditionUpload.GetRunEndTime")
            endTime = getRunEndTimeDAO.execute(run, transaction = False)

            if now < endTime + timeout:
                break

    return

def uploadToDropbox(condFiles, dropboxHost, validationMode, username, password):
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
            if not filesDict.has_key(filenamePrefix):
                filesDict[filenamePrefix] = {}
            filesDict[filenamePrefix][filenameExt] = condFile

    for filenamePrefix in filesDict.keys():

        sqliteFile = filesDict[filenamePrefix]['db']
        metaFile = filesDict[filenamePrefix]['txt']

        completeFiles.extend( uploadPayload(filenamePrefix, sqliteFile, metaFile,
                                            dropboxHost, validationMode,
                                            username, password) )

    return completeFiles

def uploadPayload(filenamePrefix, sqliteFile, metaFile, dropboxHost, validationMode, username, password):
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

    eosPrefix = "root://eoscms//eos/cms"
    sqliteFile['pfn'] = eosPrefix + sqliteFile['lfn']
    metaFile['pfn'] = eosPrefix + metaFile['lfn']

    command = "xrdcp -s -f %s %s" % (sqliteFile['pfn'], filenameDB)
    p = subprocess.Popen(command, shell = True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    output = p.communicate()[0]
    if p.returncode > 0:
        logging.error("Failure during copy from EOS: %s" % output)
        logging.error("  ==> Upload failed for payload %s" % filenamePrefix)
        inputCopied = False
    else:
        files2delete.append(filenameDB)

    command = "xrdcp -s -f %s %s" % (metaFile['pfn'], filenameTXT)
    p = subprocess.Popen(command, shell = True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    output = p.communicate()[0]
    if p.returncode > 0:
        logging.error("Failure during copy from EOS: %s" % output)
        logging.error("  ==> Upload failed for payload %s" % filenamePrefix)
        inputCopied = False
    else:
        files2delete.append(filenameTXT)

    # select the right destination db depending
    # on whether we are in validation mode
    if inputCopied:
        fin = open(filenameTXT)
        lines = fin.readlines()
        fin.close()
        fout = open(filenameTXT, 'w')
        if validationMode:
            fout.writelines( [ line.replace('prepMetaData ', '', 1) for line in lines if 'prodMetaData ' not in line] )
        else:
            fout.writelines( [ line.replace('prodMetaData ', '', 1) for line in lines if 'prepMetaData ' not in line] )
        fout.close()

        os.chmod(filenameDB, stat.S_IREAD | stat.S_IWRITE | stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)
        os.chmod(filenameTXT, stat.S_IREAD | stat.S_IWRITE | stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)

        #
        # currently fails because cmst1 does not have permission to write on EOS
        #
        #command = "xrdcp -s -f %s %s" % (filenameTXT, metaFile['pfn'] + ".uploaded")
        #p = subprocess.Popen(command, shell = True,
        #                     stdout=subprocess.PIPE,
        #                     stderr=subprocess.STDOUT)
        #output = p.communicate()[0]
        #if p.returncode > 0:
        #    logging.error("Failure during copy to EOS: %s" % output)
        #    logging.error("  ==> Upload failed for payload %s" % filenamePrefix)

        if username == None or password == None:
            completeFiles.append(sqliteFile)
            completeFiles.append(metaFile)
            logging.info("No username/password provided for DropBox upload...")
            logging.info("  ==> Upload skipped for payload %s" % filenamePrefix)
        else:
            uploadStatus = True
            try:
                upload.uploadTier0Files([filenameDB], username, password)
            except:
                logging.exception("Something went wrong with the Dropbox upload...")
                
            if uploadStatus:
                completeFiles.append(sqliteFile)
                completeFiles.append(metaFile)
                logging.info("  ==> Upload succeeded for payload %s" % filenamePrefix)
            else:
                logging.error("  ==> Upload failed for payload %s" % filenamePrefix)

    for file2delete in files2delete:
        os.remove(file2delete)

    return completeFiles
