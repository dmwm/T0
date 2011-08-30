"""
_Create_

Implementation of Create for Oracle

"""

import threading

from WMCore.Database.DBCreator import DBCreator

class Create(DBCreator):

    def __init__(self, logger = None, dbi = None):
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

        self.create[0] = \
            """CREATE TABLE cmssw_version (
                 id   int          not null,
                 name varchar(255) not null,
                 primary key(id)
               )"""

        self.create[1] = \
            """CREATE TABLE stream (
                 id    int            not null,
                 name  varchar(255)   not null,
                 primary key(id)
               )"""

        self.create[2] = \
            """CREATE TABLE processing_style (
                 id    int          not null,
                 name  varchar(255) not null,
                 primary key(id)
               )"""

        self.create[3] = \
            """CREATE TABLE run_status (
                 id      int           not null,
                 name    varchar(25)   not null,
                 primary key(id)
               )"""

        self.create[4] = \
            """CREATE TABLE run (
                 run_id             int            not null,
                 run_version        int            not null,
                 repack_version     int            not null,
                 express_version    int            not null,
                 run_status         int            not null,
                 last_updated       int            default 0 not null,
                 reco_started       int            default 0 not null,
                 express_started    int            default 0 not null,
                 hltkey             varchar(255)   not null,
                 start_time         int            not null,
                 end_time           int            default 0 not null,
                 close_time         int            default 0 not null,
                 lumicount          int            default 0 not null,
                 reco_timeout       int            default 0 not null,
                 reco_lock_timeout  int            default 0 not null,
                 process            varchar(255),
                 acq_era            varchar(255),
                 primary key(run_id)
               )"""

        self.create[5] = \
            """CREATE TABLE lumi_section (
                 run_id      int   not null,
                 lumi_id     int   not null,
                 primary key(run_id, lumi_id)
               )"""

        self.create[6] = \
            """CREATE TABLE lumi_section_closed (
                 run_id      int   not null,
                 lumi_id     int   not null,
                 stream_id   int   not null,
                 filecount   int   not null,
                 insert_time int   not null,
                 close_time  int   default 0 not null,
                 primary key(run_id, lumi_id, stream_id)
               )"""

        self.create[7] = \
            """CREATE TABLE lumi_section_split_active (
                 run_id      int   not null,
                 lumi_id     int   not null,
                 stream_id   int   not null,
                 primary key(run_id, lumi_id, stream_id)
               )"""

        self.create[8] = \
            """CREATE TABLE run_stream_primds_assoc (
                 run_id      int   not null,
                 stream_id   int   not null,
                 primds_id   int   not null,
                 primary key(run_id, stream_id, primds_id)
               )"""

        self.create[9] = \
            """CREATE TABLE run_stream_cmssw_assoc (
                 run_id           int not null,
                 stream_id        int not null,
                 run_version      int not null,
                 override_version int not null,
                 primary key(run_id, stream_id)
                )"""

        self.create[10] = \
            """CREATE TABLE run_stream_style_assoc (
                 run_id    int not null,
                 stream_id int not null,
                 style_id  int not null,
                 primary key(run_id, stream_id)
               )"""

        self.create[11] = \
            """CREATE TABLE run_stream_sub_assoc (
                 run_id       int   not null,
                 stream_id    int   not null,
                 subscription int   not null,
                 primary key(run_id, stream_id, subscription)
               )"""

        self.create[12] = \
            """CREATE TABLE streamer (
                 id              int           not null,
                 run_id          int           not null,
                 lumi_id         int           not null,
                 stream_id       int           not null,
                 insert_time     int           not null,
                 used            int           default 0,
                 deleted         int           default 0,
                 primary key(id)
               )"""

        self.indexes[0] = \
            """CREATE UNIQUE INDEX cmssw_version_uk ON cmssw_version(name)"""

        self.indexes[1] = \
            """CREATE UNIQUE INDEX stream_uk ON stream(name)"""

        self.indexes[2] = \
            """CREATE UNIQUE INDEX run_status_uk ON run_status(name)"""

        self.indexes[3] = \
            """CREATE UNIQUE INDEX processing_style_uk ON processing_style(name)"""

        self.constraints[0] = \
            """ALTER TABLE streamer
                ADD CONSTRAINT streamer_id_fk
                FOREIGN KEY (id)
                REFERENCES wmbs_file_details(id)"""

        processingStyles = { 1 : "Bulk",
                             2 : "Express",
                             3 : "Register",
                             4 : "Convert",
                             5 : "RegisterAndConvert",
                             6 : "Ignore" }
        for id, name in processingStyles.items():
            sql = """INSERT INTO processing_style
                     (ID, NAME)
                     VALUES (%d, '%s')
                     """ % (id, name)
            self.inserts["processing_style_%d" % id] = sql

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
        for id, name in runStates.items():
            sql = """INSERT INTO run_status
                     (ID, NAME)
                     VALUES (%d, '%s')
                     """ % (id, name)
            self.inserts["run_status_%d" % id] = sql

        return

    def execute(self, conn = None, transaction = None):
        """
        _execute_

        """
        DBCreator.execute(self, conn, transaction)

        return True
