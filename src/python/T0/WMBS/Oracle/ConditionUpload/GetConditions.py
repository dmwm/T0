"""
_GetConditions_

Oracle implementation of GetConditions

Return information about all run/streams that have not
finished the PCL yet and all still to be uploaded files.

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetConditions(DBFormatter):

    sql = """SELECT prompt_calib.run_id,
                    run.cond_timeout,
                    run.db_host,
                    run.valid_mode,
                    prompt_calib.stream_id,
                    prompt_calib.subscription,
                    prompt_calib_file.fileid,
                    wmbs_file_details.lfn
             FROM prompt_calib
               INNER JOIN run ON
                 run.run_id = prompt_calib.run_id
               LEFT OUTER JOIN wmbs_sub_files_acquired ON
                 wmbs_sub_files_acquired.subscription = prompt_calib.subscription
               LEFT OUTER JOIN prompt_calib_file ON
                 prompt_calib_file.fileid = wmbs_sub_files_acquired.fileid
               LEFT OUTER JOIN wmbs_file_details ON
                 wmbs_file_details.id = wmbs_sub_files_acquired.fileid
             WHERE checkForZeroState(prompt_calib.finished) = 0
             """

    def execute(self, conn = None, transaction = False):

        results = self.dbi.processData(self.sql, {},
                                       conn = conn, transaction = transaction)[0].fetchall()

        conditions = {}
        for result in results:

            run = result[0]
            streamid = result[4]

            if not conditions.has_key(run):
                conditions[run] = {}
                conditions[run]['condUploadTimeout'] = result[1]
                conditions[run]['dropboxHost'] = result[2]
                conditions[run]['validationMode'] = bool(result[3])
                conditions[run]['streams'] = {}
            if not conditions[run]['streams'].has_key(streamid):
                conditions[run]['streams'][streamid] = {}
                conditions[run]['streams'][streamid]['subscription'] = result[5]
                conditions[run]['streams'][streamid]['files'] = []

            if result[6] != None:
                conditions[run]['streams'][streamid]['files'].append( { 'fileid' : result[6],
                                                                        'lfn' : result[7] } )

        return conditions
