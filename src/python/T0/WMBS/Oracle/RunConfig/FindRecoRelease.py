"""
_FindRecoRelease_

Oracle implementation of FindRecoRelease

Return a list of tuples containing every
run,primds,fileset ready for reco release

"""

import time

from WMCore.Database.DBFormatter import DBFormatter

class FindRecoRelease(DBFormatter):

    def execute(self, conn = None, transaction = False):

        sql = """SELECT reco_release_config.run_id,
                        primary_dataset.name,
                        reco_release_config.fileset,
                        run.acq_era,
                        repack_config.proc_version
                 FROM reco_release_config
                 INNER JOIN run ON
                   run.run_id = reco_release_config.run_id
                 INNER JOIN primary_dataset ON
                   primary_dataset.id = reco_release_config.primds_id
                 INNER JOIN run_primds_stream_assoc ON
                   run_primds_stream_assoc.run_id = reco_release_config.run_id AND
                   run_primds_stream_assoc.primds_id = reco_release_config.primds_id
                 INNER JOIN repack_config ON
                   repack_config.run_id = reco_release_config.run_id AND
                   repack_config.stream_id = run_primds_stream_assoc.stream_id
                 WHERE checkForZeroState(reco_release_config.released) = 0
                 AND run.end_time + reco_release_config.delay < :NOW
                 AND run.end_time > 0
                 """

        binds = { 'NOW' : int(time.time()) }

        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)[0].fetchall()

        recoRelease = []
        for result in results:
            recoRelease.append((result[0],
                                result[1],
                                result[2],
                                result[3],
                                result[4]))

        return recoRelease
