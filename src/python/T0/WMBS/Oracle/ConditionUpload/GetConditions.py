"""
_GetConditions_

Oracle implementation of GetConditions

Return information about all run/streams that have not
finished the PCL yet and all still to be uploaded files.

"""

from WMCore.Database.DBFormatter import DBFormatter

class GetConditions(DBFormatter):

    sql = """SELECT prompt_calib.run_id,
                    prompt_calib.stream_id,
                    prompt_calib.subscription,
                    prompt_calib_file.fileid,
                    wmbs_file_details.lfn
             FROM prompt_calib
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
            streamid = result[1]

            if not conditions.has_key(run):
                conditions[run] = {}
            if not conditions[run].has_key(streamid):
                conditions[run][streamid] = {}
                conditions[run][streamid]['subscription'] = result[2]
                conditions[run][streamid]['files'] = []

            if result[3] != None:
                conditions[run][streamid]['files'].append( { 'fileid' : result[3],
                                                             'pfn' : result[4] } )

        return conditions
