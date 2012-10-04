"""
_GetConditions_

Oracle implementation of GetConditions

Return all expected and exisiting condition payloads for
runs and streams that don't have completed  the PCL yet.

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetConditions(DBFormatter):

    sql = """SELECT prompt_calib.run_id,
                    stream.name,
                    prompt_calib.finished,
                    prompt_calib_file.fileid,
                    wmbs_sub_files_acquired.subscription,
                    wmbs_file_details.lfn
             FROM prompt_calib
               INNER JOIN run ON
                 run.run_id = prompt_calib.run_id
               INNER JOIN stream ON
                 stream.id = prompt_calib.stream_id
               LEFT OUTER JOIN prompt_calib_file ON
                 prompt_calib_file.run_id = prompt_calib.run_id AND
                 prompt_calib_file.stream_id = prompt_calib.stream_id
               LEFT OUTER JOIN wmbs_sub_files_acquired ON
                 wmbs_sub_files_acquired.fileid = prompt_calib_file.fileid
               LEFT OUTER JOIN wmbs_file_details ON
                 wmbs_file_details.id = wmbs_sub_files_acquired.fileid
             WHERE checkForZeroOneState(prompt_calib.finished) IN (0,1)
             """

    def execute(self, conn = None, transaction = False):

        results = self.dbi.processData(self.sql, {},
                                       conn = conn, transaction = transaction)[0].fetchall()

        conditions = {}
        for result in results:

            run = result[0]
            stream = result[1]

            if not conditions.has_key(run):
                conditions[run] = {}
            if not conditions[run].has_key(stream):
                conditions[run][stream] = {}
                conditions[run][stream]['finished'] = result[2]
                conditions[run][stream]['files'] = []

            conditions[run][stream]['files'].append( { 'fileid' : result[3],
                                                       'subscription' : result[4],
                                                       'pfn' : result[5] } )

        return conditions
