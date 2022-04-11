"""
_Create_

Implementation of Create for Oracle

"""

import threading

from WMCore.Database.DBCreator import DBCreator

class Create(DBCreator):

    def __init__(self, logger = None, dbi = None, params = None):
        """
        _init_

        Call the DBCreator constructor and initialize the schema

        """
        myThread = threading.currentThread()
        if logger == None:
            logger = myThread.logger
        if dbi == None:
            dbi = myThread.dbi

        DBCreator.__init__(self, logger, dbi)

        #
        # Tables, functions, procedures and sequences
        #
        self.create[len(self.create)] = \
            """CREATE TABLE t0_config (
                 run_id   int           not null,
                 config   varchar2(255) not null,
                 primary key(run_id)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE t0_deployment_id (
                 name   varchar2(15)  not null,
                 id     int           not null,
                 primary key(name),
                 constraint CK_DEPLOY_ID CHECK (name='deployment_id')
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE run_status (
                 id     int          not null,
                 name   varchar2(25) not null,
                 primary key(id),
                 constraint run_sta_name_uq unique(name)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE processing_style (
                 id     int          not null,
                 name   varchar2(25) not null,
                 primary key(id),
                 constraint pro_sty_name_uq unique(name)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE event_scenario (
                 id     int          not null,
                 name   varchar2(50) not null,
                 primary key(id),
                 constraint eve_sce_name_uq unique(name)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE cmssw_version (
                 id     int           not null,
                 name   varchar2(255) not null,
                 primary key(id),
                 constraint cms_ver_name_uq unique(name)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE stream (
                 id     int           not null,
                 name   varchar2(255) not null,
                 primary key(id),
                 constraint str_name_uq unique(name)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE trigger_label (
                 id     int           not null,
                 name   varchar2(255) not null,
                 primary key(id),
                 constraint tri_lab_name_uq unique(name)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE primary_dataset (
                 id     int           not null,
                 name   varchar2(255) not null,
                 primary key(id),
                 constraint pri_dat_name_uq unique(name)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE storage_node (
                 id     int           not null,
                 name   varchar2(255) not null,
                 primary key(id),
                 constraint sto_nod_name_uq unique(name)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE run (
                 run_id             int           not null,
                 status             int           default 1 not null,
                 express_released   int           default 0 not null,
                 hltkey             varchar2(255) not null,
                 start_time         int           default 0 not null,
                 stop_time          int           default 0 not null,
                 close_time         int           default 0 not null,
                 lumicount          int           default 0 not null,
                 in_datasvc         int           default 0 not null,
                 process            varchar2(255),
                 acq_era            varchar2(255),
                 backfill           varchar2(255),
                 bulk_data_type     varchar2(50),
                 dqmuploadurl       varchar2(255),
                 ah_timeout         int,
                 ah_cond_lfnbase    varchar2(255),
                 ah_lumi_url        varchar2(255),
                 cond_timeout       int,
                 db_host            varchar2(255),
                 valid_mode         int,
                 primary key(run_id)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE run_trig_primds_assoc (
                 run_id      int not null,
                 primds_id   int not null,
                 trig_id     int not null,
                 primary key(run_id, primds_id, trig_id)
               ) ORGANIZATION INDEX COMPRESS 2"""

        self.create[len(self.create)] = \
            """CREATE TABLE run_primds_stream_assoc (
                 run_id      int not null,
                 primds_id   int not null,
                 stream_id   int not null,
                 primary key(run_id, primds_id)
               )"""

        self.create[len(self.create)] = \
            """CREATE TABLE run_primds_scenario_assoc (
                 run_id        int not null,
                 primds_id     int not null,
                 scenario_id   int not null,
                 primary key(run_id, primds_id)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE run_stream_style_assoc (
                 run_id      int not null,
                 stream_id   int not null,
                 style_id    int not null,
                 primary key(run_id, stream_id)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE run_stream_cmssw_assoc (
                 run_id             int not null,
                 stream_id          int not null,
                 online_version     int not null,
                 primary key(run_id, stream_id)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE run_stream_fileset_assoc (
                 run_id      int not null,
                 stream_id   int not null,
                 fileset     int not null,
                 primary key(run_id, stream_id),
                 constraint run_str_fil_ass_fil_uq unique(fileset)
                   using index
                     (create unique index idx_run_stream_fileset_assoc_1 on run_stream_fileset_assoc (fileset))
               )"""

        self.create[len(self.create)] = \
            """CREATE TABLE run_stream_done (
                 run_id      int not null,
                 stream_id   int not null,
                 in_datasvc  int default 0 not null,
                 primary key(run_id, stream_id)
               )"""

        self.create[len(self.create)] = \
            """CREATE TABLE reco_release_config (
                 run_id         int not null,
                 primds_id      int not null,
                 in_datasvc     int default 0 not null,
                 released       int default 0 not null,
                 fileset        int not null,
                 delay          int not null,
                 delay_offset   int not null,
                 primary key(run_id, primds_id),
                 constraint rec_rel_con_fil_uq unique(fileset)
                   using index
                     (create unique index idx_reco_release_config_1 on reco_release_config (fileset))
               )"""

        self.create[len(self.create)] = \
            """CREATE TABLE stream_special_primds_assoc (
                 stream_id   int not null,
                 primds_id   int not null,
                 primary key(stream_id)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE lumi_section (
                 run_id    int not null,
                 lumi_id   int not null,
                 primary key(run_id, lumi_id)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE lumi_section_closed (
                 run_id      int   not null,
                 stream_id   int   not null,
                 lumi_id     int   not null,
                 filecount   int   not null,
                 insert_time int   not null,
                 close_time  int   default 0 not null,
                 primary key(run_id, stream_id, lumi_id)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE lumi_section_split_active (
                 subscription   int not null,
                 run_id         int not null,
                 lumi_id        int not null,
                 nfiles         int not null,
                 primary key(subscription, run_id, lumi_id)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE streamer (
                 id            int not null,
                 p5_id         int not null,
                 run_id        int not null,
                 stream_id     int not null,
                 lumi_id       int not null,
                 insert_time   int not null,
                 used          int default 0 not null,
                 deleted       int default 0 not null,
                 primary key(id)
               )"""

        self.create[len(self.create)] = \
            """CREATE TABLE repack_config (
                 run_id               int          not null,
                 stream_id            int          not null,
                 proc_version         int          not null,
                 max_size_single_lumi int          not null,
                 max_size_multi_lumi  int          not null,
                 min_size             int          not null,
                 max_size             int          not null,
                 max_edm_size         int          not null,
                 max_over_size        int          not null,
                 max_events           int          not null,
                 max_files            int          not null,
                 cmssw_id             int          not null,
                 scram_arch           varchar2(50) not null,
                 primary key (run_id, stream_id)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE express_config (
                 run_id          int           not null,
                 stream_id       int           not null,
                 in_datasvc      int           default 0 not null,
                 proc_version    int           not null,
                 write_tiers     varchar2(255),
                 write_dqm       int           not null,
                 global_tag      varchar2(255) not null,
                 max_rate        int           not null,
                 max_events      int           not null,
                 max_size        int           not null,
                 max_files       int           not null,
                 max_latency     int           not null,
                 dqm_interval    int           not null,
                 cmssw_id        int           not null,
                 scram_arch      varchar2(50)  not null,
                 data_type       varchar2(50)  not null,
                 reco_cmssw_id   int,
                 multicore       int,
                 reco_scram_arch varchar2(50),
                 alca_skim       varchar2(700),
                 dqm_seq         varchar2(700),
                 primary key (run_id, stream_id)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE prompt_calib (
                 run_id        int not null,
                 stream_id     int not null,
                 num_producer  int not null,
                 finished      int default 0 not null,
                 primary key (run_id, stream_id)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE prompt_calib_file (
                 run_id        int not null,
                 stream_id     int not null,
                 fileid        int not null,
                 subscription  int not null,
                 primary key (run_id, stream_id, fileid)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE reco_config (
                 run_id         int            not null,
                 primds_id      int            not null,
                 in_datasvc     int            default 0 not null,
                 do_reco        int            not null,
                 reco_split     int            not null,
                 write_reco     int            not null,
                 write_dqm      int            not null,
                 write_aod      int            not null,
                 write_miniaod  int            not null,
                 proc_version   int            not null,
                 cmssw_id       int            not null,
                 scram_arch     varchar2(50)   not null,
                 global_tag     varchar2(255)  not null,
                 multicore      int,
                 alca_skim      varchar2(700),
                 physics_skim   varchar2(700),
                 dqm_seq        varchar2(700),
                 primary key (run_id, primds_id)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE phedex_config (
                 run_id            int not null,
                 primds_id         int not null,
                 archival_node_id  int,
                 tape_node_id      int,
                 disk_node_id      int,
                 disk_node_reco_id int,
                 primary key (run_id, primds_id)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE workflow_monitoring (
                 workflow   int not null,
                 tracked    int default 0 not null,
                 closeout   int default 0 not null,  
                 primary key (workflow)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE TABLE dataset_locked (
                 dataset_id  int not null,
                 primary key (dataset_id)
               ) ORGANIZATION INDEX"""

        self.create[len(self.create)] = \
            """CREATE FUNCTION checkForZeroState (value IN int)
               RETURN int DETERMINISTIC IS
               BEGIN
                 IF value = 0 THEN
                   RETURN 0;
                 ELSE
                   RETURN NULL;
                 END IF;
               END checkForZeroState;
               """

        self.create[len(self.create)] = \
            """CREATE FUNCTION checkForZeroOneState (value IN int)
               RETURN int DETERMINISTIC IS
               BEGIN
                 IF value = 0 THEN
                   RETURN 0;
                 ELSIF value = 1 THEN
                   RETURN 1;
                 ELSE
                   RETURN NULL;
                 END IF;
               END checkForZeroOneState;
               """

        self.create[len(self.create)] = \
            """CREATE FUNCTION checkForZeroOneTwoState (value IN int)
               RETURN int DETERMINISTIC IS
               BEGIN
                 IF value = 0 THEN
                   RETURN 0;
                 ELSIF value = 1 THEN
                   RETURN 1;
                 ELSIF value = 2 THEN
                   RETURN 2;
                 ELSE
                   RETURN NULL;
                 END IF;
               END checkForZeroOneTwoState;
               """

        self.create[len(self.create)] = \
            """CREATE SEQUENCE cmssw_version_SEQ
               START WITH 1
               INCREMENT BY 1
               NOMAXVALUE
               CACHE 10
               """

        self.create[len(self.create)] = \
            """CREATE SEQUENCE stream_SEQ
               START WITH 1
               INCREMENT BY 1
               NOMAXVALUE
               CACHE 10
               """

        self.create[len(self.create)] = \
            """CREATE SEQUENCE trigger_label_SEQ
               START WITH 1
               INCREMENT BY 1
               NOMAXVALUE
               CACHE 100
               """

        self.create[len(self.create)] = \
            """CREATE SEQUENCE primary_dataset_SEQ
               START WITH 1
               INCREMENT BY 1
               NOMAXVALUE
               CACHE 100
               """

        self.create[len(self.create)] = \
            """CREATE SEQUENCE storage_node_SEQ
               START WITH 1
               INCREMENT BY 1
               NOMAXVALUE
               CACHE 100
               """

        #
        # Indexes
        #
        #
        # Usual rules is to put an index on all FK. I don't follow it
        # strictly here because some tables are only used rarely and
        # with well defined filter conditions. In these cases I might
        # just add an index on the condition I need.
        #
        self.indexes[len(self.indexes)] = \
            """CREATE INDEX idx_run_1 ON run (checkForZeroState(express_released))"""

        self.indexes[len(self.indexes)] = \
            """CREATE INDEX idx_run_2 ON run (status)"""

        self.indexes[len(self.indexes)] = \
            """CREATE INDEX idx_run_3 ON run (checkForZeroState(in_datasvc))"""

        self.indexes[len(self.indexes)] = \
            """CREATE INDEX idx_run_primds_stream_1 ON run_primds_stream_assoc (run_id, stream_id)"""

        self.indexes[len(self.indexes)] = \
            """CREATE INDEX idx_run_stream_done_1 ON run_stream_done (checkForZeroState(in_datasvc))"""

        self.indexes[len(self.indexes)] = \
            """CREATE INDEX idx_reco_release_config_2 ON reco_release_config (checkForZeroOneTwoState(in_datasvc))"""

        self.indexes[len(self.indexes)] = \
            """CREATE INDEX idx_reco_release_config_3 ON reco_release_config (checkForZeroOneState(released))"""

        self.indexes[len(self.indexes)] = \
            """CREATE INDEX idx_lumi_section_closed_1 ON lumi_section_closed (checkForZeroState(close_time))"""

        self.indexes[len(self.indexes)] = \
            """CREATE INDEX idx_streamer_1 ON streamer (run_id, stream_id, lumi_id)"""

        self.indexes[len(self.indexes)] = \
            """CREATE INDEX idx_streamer_2 ON streamer (checkForZeroState(used))"""

        self.indexes[len(self.indexes)] = \
            """CREATE INDEX idx_streamer_3 ON streamer (checkForZeroState(deleted))"""

        self.indexes[len(self.indexes)] = \
            """CREATE INDEX idx_prompt_calib_1 ON prompt_calib (checkForZeroState(finished))"""

        self.indexes[len(self.indexes)] = \
            """CREATE INDEX idx_express_config_1 ON express_config (checkForZeroState(in_datasvc))"""

        self.indexes[len(self.indexes)] = \
            """CREATE INDEX idx_reco_config_1 ON reco_config (checkForZeroState(in_datasvc))"""

        self.indexes[len(self.indexes)] = \
            """CREATE INDEX idx_workflow_monitoring_0 ON workflow_monitoring (checkForZeroState(tracked))"""

        self.indexes[len(self.indexes)] = \
            """CREATE INDEX idx_workflow_monitoring_1 ON workflow_monitoring (checkForZeroState(closeout))"""
        #
        # Constraints
        #
        self.constraints[len(self.constraints)] = \
            """ALTER TABLE t0_config
                 ADD CONSTRAINT t0_conf_run_id_fk
                 FOREIGN KEY (run_id)
                 REFERENCES run(run_id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE run
                 ADD CONSTRAINT run_sta_fk
                 FOREIGN KEY (status)
                 REFERENCES run_status(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE run_trig_primds_assoc
                 ADD CONSTRAINT run_tri_pri_run_id_fk
                 FOREIGN KEY (run_id)
                 REFERENCES run(run_id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE run_trig_primds_assoc
                 ADD CONSTRAINT run_tri_pri_pri_id_fk
                 FOREIGN KEY (primds_id)
                 REFERENCES primary_dataset(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE run_trig_primds_assoc
                 ADD CONSTRAINT run_tri_pri_tri_id_fk
                 FOREIGN KEY (trig_id)
                 REFERENCES trigger_label(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE run_primds_stream_assoc
                 ADD CONSTRAINT run_pri_tri_run_id_fk
                 FOREIGN KEY (run_id)
                 REFERENCES run(run_id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE run_primds_stream_assoc
                 ADD CONSTRAINT run_pri_tri_pri_id_fk
                 FOREIGN KEY (primds_id)
                 REFERENCES primary_dataset(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE run_primds_stream_assoc
                 ADD CONSTRAINT run_pri_tri_str_id_fk
                 FOREIGN KEY (stream_id)
                 REFERENCES stream(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE run_primds_scenario_assoc
                 ADD CONSTRAINT run_pri_sce_run_id_fk
                 FOREIGN KEY (run_id)
                 REFERENCES run(run_id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE run_primds_scenario_assoc
                 ADD CONSTRAINT run_pri_sce_pri_id_fk
                 FOREIGN KEY (primds_id)
                 REFERENCES primary_dataset(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE run_primds_scenario_assoc
                 ADD CONSTRAINT run_pri_sce_sce_id_fk
                 FOREIGN KEY (scenario_id)
                 REFERENCES event_scenario(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE run_stream_style_assoc
                 ADD CONSTRAINT run_str_sty_run_id_fk
                 FOREIGN KEY (run_id)
                 REFERENCES run(run_id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE run_stream_style_assoc
                 ADD CONSTRAINT run_str_sty_str_id_fk
                 FOREIGN KEY (stream_id)
                 REFERENCES stream(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE run_stream_style_assoc
                 ADD CONSTRAINT run_str_sty_sty_id_fk
                 FOREIGN KEY (style_id)
                 REFERENCES processing_style(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE run_stream_cmssw_assoc
                 ADD CONSTRAINT run_str_cms_run_id_fk
                 FOREIGN KEY (run_id)
                 REFERENCES run(run_id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE run_stream_cmssw_assoc
                 ADD CONSTRAINT run_str_cms_str_id_fk
                 FOREIGN KEY (stream_id)
                 REFERENCES stream(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE run_stream_cmssw_assoc
                 ADD CONSTRAINT run_str_cms_onl_ver_fk
                 FOREIGN KEY (online_version)
                 REFERENCES cmssw_version(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE run_stream_fileset_assoc
                 ADD CONSTRAINT run_str_fil_run_id_fk
                 FOREIGN KEY (run_id)
                 REFERENCES run(run_id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE run_stream_fileset_assoc
                 ADD CONSTRAINT run_str_fil_str_id_fk
                 FOREIGN KEY (stream_id)
                 REFERENCES stream(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE run_stream_fileset_assoc
                 ADD CONSTRAINT run_str_fil_fil_id_fk
                 FOREIGN KEY (fileset)
                 REFERENCES wmbs_fileset(id)
                 ON DELETE CASCADE"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE run_stream_done
                 ADD CONSTRAINT run_str_don_run_id_fk
                 FOREIGN KEY (run_id)
                 REFERENCES run(run_id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE run_stream_done
                 ADD CONSTRAINT run_str_don_str_id_fk
                 FOREIGN KEY (stream_id)
                 REFERENCES stream(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE reco_release_config
                 ADD CONSTRAINT rec_rel_con_run_id_fk
                 FOREIGN KEY (run_id)
                 REFERENCES run(run_id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE reco_release_config
                 ADD CONSTRAINT rec_rel_con_pri_id_fk
                 FOREIGN KEY (primds_id)
                 REFERENCES primary_dataset(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE reco_release_config
                 ADD CONSTRAINT rec_rel_con_fil_id_fk
                 FOREIGN KEY (fileset)
                 REFERENCES wmbs_fileset(id)
                 ON DELETE CASCADE"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE stream_special_primds_assoc
                 ADD CONSTRAINT str_spe_pri_str_id_fk
                 FOREIGN KEY (stream_id)
                 REFERENCES stream(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE stream_special_primds_assoc
                 ADD CONSTRAINT str_spe_pri_pri_id_fk
                 FOREIGN KEY (primds_id)
                 REFERENCES primary_dataset(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE lumi_section
                 ADD CONSTRAINT lum_sec_run_id_fk
                 FOREIGN KEY (run_id)
                 REFERENCES run(run_id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE lumi_section_closed
                 ADD CONSTRAINT lum_sec_clo_rl_id_fk
                 FOREIGN KEY (run_id, lumi_id)
                 REFERENCES lumi_section(run_id, lumi_id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE lumi_section_closed
                 ADD CONSTRAINT lum_sec_clo_stre_id_fk
                 FOREIGN KEY (stream_id)
                 REFERENCES stream(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE lumi_section_split_active
                 ADD CONSTRAINT lum_sec_spli_act_rl_id_fk
                 FOREIGN KEY (run_id, lumi_id)
                 REFERENCES lumi_section(run_id, lumi_id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE lumi_section_split_active
                 ADD CONSTRAINT lum_sec_spli_act_stre_id_fk
                 FOREIGN KEY (subscription)
                 REFERENCES wmbs_subscription(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE streamer
                 ADD CONSTRAINT str_run_id_fk
                 FOREIGN KEY (run_id)
                 REFERENCES run(run_id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE streamer
                 ADD CONSTRAINT str_rl_id_fk
                 FOREIGN KEY (run_id, lumi_id)
                 REFERENCES lumi_section(run_id, lumi_id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE streamer
                 ADD CONSTRAINT str_str_id_fk
                 FOREIGN KEY (stream_id)
                 REFERENCES stream(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE repack_config
                 ADD CONSTRAINT rep_con_run_id_fk
                 FOREIGN KEY (run_id)
                 REFERENCES run(run_id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE repack_config
                 ADD CONSTRAINT rep_con_str_id_fk
                 FOREIGN KEY (stream_id)
                 REFERENCES stream(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE express_config
                 ADD CONSTRAINT exp_con_run_id_fk
                 FOREIGN KEY (run_id)
                 REFERENCES run(run_id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE express_config
                 ADD CONSTRAINT exp_con_str_id_fk
                 FOREIGN KEY (stream_id)
                 REFERENCES stream(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE express_config
                 ADD CONSTRAINT exp_con_cms_id_fk
                 FOREIGN KEY (cmssw_id)
                 REFERENCES cmssw_version(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE prompt_calib
                 ADD CONSTRAINT pro_cal_run_id_fk
                 FOREIGN KEY (run_id)
                 REFERENCES run(run_id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE prompt_calib
                 ADD CONSTRAINT pro_cal_str_id_fk
                 FOREIGN KEY (stream_id)
                 REFERENCES stream(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE prompt_calib_file
                 ADD CONSTRAINT pro_cal_fil_run_id_fk
                 FOREIGN KEY (run_id)
                 REFERENCES run(run_id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE prompt_calib_file
                 ADD CONSTRAINT pro_cal_fil_str_id_fk
                 FOREIGN KEY (stream_id)
                 REFERENCES stream(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE prompt_calib_file
                 ADD CONSTRAINT pro_cal_fil_fil_id_fk
                 FOREIGN KEY (fileid)
                 REFERENCES wmbs_file_details(id)
                 ON DELETE CASCADE"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE prompt_calib_file
                 ADD CONSTRAINT pro_cal_fil_sub_fk
                 FOREIGN KEY (subscription)
                 REFERENCES wmbs_subscription(id)
                 ON DELETE CASCADE"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE reco_config
                 ADD CONSTRAINT rec_con_run_id_fk
                 FOREIGN KEY (run_id)
                 REFERENCES run(run_id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE reco_config
                 ADD CONSTRAINT rec_con_primds_id_fk
                 FOREIGN KEY (primds_id)
                 REFERENCES primary_dataset(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE reco_config
                 ADD CONSTRAINT rec_con_cms_id_fk
                 FOREIGN KEY (cmssw_id)
                 REFERENCES cmssw_version(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE phedex_config
                 ADD CONSTRAINT phe_con_run_id_fk
                 FOREIGN KEY (run_id)
                 REFERENCES run(run_id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE phedex_config
                 ADD CONSTRAINT phe_con_primds_id_fk
                 FOREIGN KEY (primds_id)
                 REFERENCES primary_dataset(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE phedex_config
                 ADD CONSTRAINT phe_con_arc_nod_id_fk
                 FOREIGN KEY (archival_node_id)
                 REFERENCES storage_node(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE phedex_config
                 ADD CONSTRAINT phe_con_tap_nod_id_fk
                 FOREIGN KEY (tape_node_id)
                 REFERENCES storage_node(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE phedex_config
                 ADD CONSTRAINT phe_con_dis_nod_id_fk
                 FOREIGN KEY (disk_node_id)
                 REFERENCES storage_node(id)"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE workflow_monitoring
                 ADD CONSTRAINT wor_mon_wor_fk
                 FOREIGN KEY (workflow)
                 REFERENCES wmbs_workflow(id)
                 ON DELETE CASCADE"""

        self.constraints[len(self.constraints)] = \
            """ALTER TABLE dataset_locked
                 ADD CONSTRAINT dat_loc
                 FOREIGN KEY (dataset_id)
                 REFERENCES dbsbuffer_dataset(id)
                 ON DELETE CASCADE"""

        subTypes = ["Express", "Repack"]
        for name in subTypes:
            sql = """INSERT INTO wmbs_sub_types
                     (ID, NAME)
                     SELECT wmbs_sub_types_SEQ.nextval, '%s'
                     FROM DUAL
                     WHERE NOT EXISTS (
                       SELECT id FROM wmbs_sub_types WHERE name = '%s'
                     )
                     """ % (name, name)
            self.inserts[len(self.inserts)] = sql

        runStates = { 1 : "Active",
                      2 : "CloseOutRepack",
                      3 : "CloseOutRepackMerge",
                      4 : "CloseOutPromptReco",
                      5 : "CloseOutRecoMerge",
                      6 : "CloseOutAlcaSkim",
                      7 : "CloseOutAlcaSkimMerge",
                      8 : "CloseOutExport",
                      9 : "CloseOutT1Skimming",
                      10 : "Complete" }
        for id, name in list(runStates.items()):
            sql = """INSERT INTO run_status
                     (ID, NAME)
                     VALUES (%d, '%s')
                     """ % (id, name)
            self.inserts[len(self.inserts)] = sql

        processingStyles = { 1 : "Bulk",
                             2 : "Express",
                             3 : "Register",
                             4 : "Convert",
                             5 : "RegisterAndConvert",
                             6 : "Ignore" }
        for id, name in list(processingStyles.items()):
            sql = """INSERT INTO processing_style
                     (ID, NAME)
                     VALUES (%d, '%s')
                     """ % (id, name)
            self.inserts[len(self.inserts)] = sql

        eventScenarios = { 1 : "pp",
                           2 : "cosmics",
                           3 : "hcalnzs",
                           4 : "HeavyIons",
                           5 : "AlCaTestEnable",
                           6 : "AlCaP0",
                           7 : "AlCaPhiSymEcal",
                           8 : "AlCaLumiPixels",
                           9 : "DataScouting",
                           10 : "ppRun2",
                           11 : "cosmicsRun2",
                           12 : "hcalnzsRun2",
                           13 : "ppRun2B0T",
                           14 : "AlCa",
                           15 : "ppRun2at50ns",
                           16 : "HeavyIonsRun2",
                           17 : "ppEra_Run2_25ns",
                           18 : "cosmicsEra_Run2_25ns",
                           19 : "hcalnzsEra_Run2_25ns",
                           20 : "ppEra_Run2_2016",
                           21 : "cosmicsEra_Run2_2016",
                           22 : "hcalnzsEra_Run2_2016",
                           23 : "ppEra_Run2_2016_trackingLowPU",
                           24 : "ppEra_Run2_2016_pA",
                           25 : "ppEra_Run2_2017",
                           26 : "cosmicsEra_Run2_2017",
                           27 : "hcalnzsEra_Run2_2017",
                           28 : "ppEra_Run2_2017_trackingOnly",
                           29 : "ppEra_Run2_2017_ppRef",
                           30 : "cosmicsEra_Run2_2018",
                           31 : "hcalnzsEra_Run2_2018",
                           32 : "ppEra_Run2_2018",
                           33 : "trackingOnlyEra_Run2_2018",
                           34 : "ppEra_Run2_2018_pp_on_AA",
                           35 : "hcalnzsEra_Run2_2018_pp_on_AA",
                           36 : "trackingOnlyEra_Run2_2018_pp_on_AA",
                           37 : "ppEra_Run3",
                           38 : "cosmicsEra_Run3",
                           39 : "hcalnzsEra_Run3",
                           40 : "trackingOnlyEra_Run3",
                           41 : "AlCaLumiPixels_Run3",
                           42 : "AlCaPhiSymEcal_Nano" }
        for id, name in list(eventScenarios.items()):
            sql = """INSERT INTO event_scenario
                     (ID, NAME)
                     VALUES (%d, '%s')
                     """ % (id, name)
            self.inserts[len(self.inserts)] = sql

        return

    def execute(self, conn = None, transaction = None):
        """
        _execute_

        """
        DBCreator.execute(self, conn, transaction)

        return True
