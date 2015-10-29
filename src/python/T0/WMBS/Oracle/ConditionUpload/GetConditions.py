"""
_GetConditions_

Oracle implementation of GetConditions

Return information about all run/streams that have not
finished the PCL yet and all still to be uploaded files.

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetConditions(DBFormatter):

    sqlNotFinished = """SELECT prompt_calib.run_id,
                               run.cond_timeout,
                               run.db_host,
                               run.valid_mode,
                               prompt_calib.stream_id,
                               prompt_calib_file.fileid,
                               prompt_calib_file.subscription,
                               wmbs_file_details.lfn
                        FROM prompt_calib
                        INNER JOIN run ON
                          run.run_id = prompt_calib.run_id
                        LEFT OUTER JOIN prompt_calib_file ON
                          prompt_calib_file.run_id = prompt_calib.run_id AND
                          prompt_calib_file.stream_id = prompt_calib.stream_id
                        LEFT OUTER JOIN wmbs_sub_files_acquired ON
                          wmbs_sub_files_acquired.fileid = prompt_calib_file.fileid
                        LEFT OUTER JOIN wmbs_file_details ON
                          wmbs_file_details.id = wmbs_sub_files_acquired.fileid
                        WHERE checkForZeroState(prompt_calib.finished) = 0
                        """

    sqlFinished = """SELECT prompt_calib.run_id,
                            run.cond_timeout,
                            run.db_host,
                            run.valid_mode,
                            prompt_calib.stream_id,
                            prompt_calib_file.fileid,
                            prompt_calib_file.subscription,
                            wmbs_file_details.lfn
                     FROM prompt_calib
                     INNER JOIN run ON
                       run.run_id = prompt_calib.run_id
                     INNER JOIN prompt_calib_file ON
                       prompt_calib_file.run_id = prompt_calib.run_id AND
                       prompt_calib_file.stream_id = prompt_calib.stream_id
                     INNER JOIN wmbs_sub_files_acquired ON
                       wmbs_sub_files_acquired.fileid = prompt_calib_file.fileid
                     INNER JOIN wmbs_file_details ON
                       wmbs_file_details.id = wmbs_sub_files_acquired.fileid
                     WHERE prompt_calib.finished = 1
                     """

    def execute(self, finished, conn = None, transaction = False):

        if finished:
            results = self.dbi.processData(self.sqlFinished, {},
                                           conn = conn, transaction = transaction)[0].fetchall()
        else:
            results = self.dbi.processData(self.sqlNotFinished, {},
                                           conn = conn, transaction = transaction)[0].fetchall()

        conditions = {}
        for result in results:

            run = result[0]
            streamid = result[4]

            if run not in conditions:
                conditions[run] = {}
                conditions[run]['condUploadTimeout'] = result[1]
                conditions[run]['dropboxHost'] = result[2]
                conditions[run]['validationMode'] = bool(result[3])
                conditions[run]['streams'] = {}
            if streamid not in conditions[run]['streams']:
                conditions[run]['streams'][streamid] = []

            # only return file information for aquired files
            if result[7] != None:
                conditions[run]['streams'][streamid].append( { 'fileid' : result[5],
                                                               'subscription' : result[6],
                                                               'lfn' : result[7] } )

        return conditions
