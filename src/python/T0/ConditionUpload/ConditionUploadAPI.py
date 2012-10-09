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

from WMCore.DAOFactory import DAOFactory


def uploadConditions(timeout, dropboxHost, validationMode):
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

        for streamid in conditions[run].keys():

            # always upload files (if there are any to upload)
            condFiles = []
            uploadedFiles = []
            for condFile in conditions[run][streamid]['files']:
                condFiles.append(condFile)
            if len(condFiles) > 0:
                uploadedFiles = uploadToDropbox(condFiles, dropboxHost, validationMode)

            bindVarList = []
            for uploadedFile in uploadedFiles:
                bindVarList.append( { 'FILEID' : uploadedFile['fileid'],
                                      'SUBSCRIPTION' : conditions[run][streamid]['subscription'] } )

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
            if  conditions[run][streamid]['subscription'] != None:
                finished = isPromptCalibrationFinishedDAO.execute(conditions[run][streamid]['subscription'])
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

def uploadToDropbox(condFiles, dropboxHost, validationMode):
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
        if condFile['pfn'] == "/no/output":
            completeFiles.append(condFile)
        else:
            (filenamePrefix, filenameExt) = os.path.basename(condFile['pfn']).split('.')
            if not filesDict.has_key(filenamePrefix):
                filesDict[filenamePrefix] = {}
            filesDict[filenamePrefix][filenameExt] = condFile

    files2delete = []
    for filenamePrefix in filesDict.keys():

        sqliteFile = filesDict[filenamePrefix]['db']
        metaFile = filesDict[filenamePrefix]['txt']

        filenameDB = filenamePrefix + ".db"
        filenameTXT = filenamePrefix + ".txt"
        filenameTAR = filenamePrefix + ".tar.bz2"

        shutil.copy2(sqliteFile['pfn'], filenameDB)
        files2delete.append(filenameDB)

        # select the right destination db depending
        # on whether we are in validation mode
        fin = open(metaFile['pfn'])
        lines = fin.readlines()
        fin.close()
        fout = open(filenameTXT, 'w')
        if validationMode:
            fout.writelines( [ line.replace('destDBValidation', 'destDB', 1) for line in lines if 'destDB ' not in line] )
        else:
            fout.writelines( [ line for line in lines if 'destDBValidation ' not in line] )
        fout.close()
        files2delete.append(filenameTXT)

        os.chmod(filenameDB, stat.S_IREAD | stat.S_IWRITE | stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)
        os.chmod(filenameTXT, stat.S_IREAD | stat.S_IWRITE | stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)

        uploadStatus = True
        if validationMode:

            fout = tarfile.open(filenameTAR, "w:bz2")
            fout.add(filenameDB)
            fout.add(filenameTXT)
            fout.close()
            files2delete.append(filenameTAR)

            os.chmod(filenameTAR, stat.S_IREAD | stat.S_IWRITE | stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)

            for file2upload in [ filenameTAR ]:

                status = False
                if 0 == subprocess.call(["scp", "-p", file2upload, "%s:/tmp/" % dropboxHost]):
                    if 0 == subprocess.call(["ssh", dropboxHost, "mv /tmp/%s /DropBox_test/" % file2upload]):
                        logging.info("DropBox validation upload suceeded for %s" % file2upload)
                        status = True

                if status == False:
                    logging.error("DropBox validation upload failed for %s" % file2upload)
                    uploadStatus = False

        else:

            for file2upload in [ filenameDB, filenameTXT ]:

                status = False
                if 0 == subprocess.call(["scp", "-p", file2upload, "%s:/tmp/" % dropboxHost]):
                    if 0 == subprocess.call(["ssh", dropboxHost, "mv /tmp/%s /DropBox/" % file2upload]):
                        logging.info("DropBox upload suceeded for %s" % file2upload)
                        status = True

                if status == False:
                    logging.error("DropBox upload failed for %s" % file2upload)
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
