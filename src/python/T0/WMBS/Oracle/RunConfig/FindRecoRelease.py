"""
_FindRecoRelease_

Oracle implementation of FindRecoRelease

Take the list of passed in datasets and
their delays and delay offsets and find
all run/dataset that can be pre-released.

Pre-release goes strictly in run order since
it stops condition updates and that also happens
in strict run order. Therefore pre-release only
ever works on the lowest run that has not yet
pre-released datasets.

On pre-release update the delay and offset
in reco_release_config so that on final
release the second query can move the
status forward.

Then return information for all run/dataset
that are ready for final release.

"""
import time

from WMCore.Database.DBFormatter import DBFormatter

class FindRecoRelease(DBFormatter):

    def execute(self, datasetDelays, conn = None, transaction = False):

        now = int(time.time())

        binds = []
        for dataset, delays in list(datasetDelays.items()):
            binds.append( { 'NOW' : now,
                            'DATASET' : dataset,
                            'DELAY' : delays[0],
                            'DELAY_OFFSET' : delays[1] } )

        sql = """UPDATE (
                          SELECT reco_release_config.released AS released,
                                 reco_release_config.delay AS delay,
                                 reco_release_config.delay_offset AS delay_offset
                          FROM reco_release_config
                          INNER JOIN run ON
                            run.run_id = reco_release_config.run_id
                          INNER JOIN primary_dataset ON
                            primary_dataset.id = reco_release_config.primds_id AND
                            primary_dataset.name = :DATASET
                          WHERE checkForZeroOneState(reco_release_config.released) = 0
                          AND run.stop_time + :DELAY - :DELAY_OFFSET < :NOW
                          AND run.stop_time > 0
                          AND run.run_id = ( SELECT MIN(reco_release_config.run_id)
                                             FROM reco_release_config
                                             WHERE checkForZeroOneState(reco_release_config.released) = 0 )
                        ) t
                 SET t.released = 1,
                     t.delay = :DELAY,
                     t.delay_offset = :DELAY_OFFSET
                 """

        if len(binds) > 0:
            self.dbi.processData(sql, binds, conn = conn,
                                 transaction = transaction)

        binds = { 'NOW' : now }

        sql = """SELECT reco_release_config.run_id,
                        primary_dataset.name,
                        reco_release_config.fileset,
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
                 WHERE checkForZeroOneState(reco_release_config.released) = 1
                 AND run.stop_time + reco_release_config.delay < :NOW
                 """

        results = self.dbi.processData(sql, binds, conn = conn,
                                       transaction = transaction)[0].fetchall()

        recoRelease = {}
        for result in results:

            run = result[0]

            if run not in recoRelease:
                recoRelease[run] = []

            recoRelease[run].append((result[1],
                                     result[2],
                                     result[3]))

        return recoRelease
