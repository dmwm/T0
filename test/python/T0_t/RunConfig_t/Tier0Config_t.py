import unittest
import T0.RunConfig.Tier0Config as tier0config


class TestRetrieveStreamConfig(unittest.TestCase):

    def setUp(self):
        self.config = tier0config.createTier0Config()

    def test_createTier0Config(self):
        # Check some key values in the Global section
        self.assertEqual(self.config.Global.ProcessingSite, "T2_CH_CERN")
        self.assertEqual(self.config.Global.StreamerPNN, "T0_CH_CERN_Disk")
        self.assertEqual(self.config.Global.StorageSite, "T0_CH_CERN_Disk")
        self.assertEqual(self.config.Global.DQMDataTier, "DQMIO")
        self.assertEqual(self.config.Global.BaseRequestPriority, 150000)
        self.assertEqual(self.config.Global.EnableUniqueWorkflowName, False)
        self.assertEqual(self.config.Global.DeploymentID, 1)

    def test_retrieveStreamConfig(self):

        streamName = "Express"
        options = {
            "versionOverride": {"CMSSW_12_0_0": 1},
            "scenario": "ppEra",
            "data_tiers": ["RAW", "RECO"],
            "global_tag": "GLOBALTAG::All",
            "global_tag_connect": "GTCONNECT",
            "reco_version": "CMSSW_12_0_1",
            "multicore": 8,
            "alca_producers": ["AlcaProducer1", "AlcaProducer2"],
            "write_dqm": True,
            "dqm_sequences": ["DQMSeq1", "DQMSeq2"],
            "proc_ver": 2,
            "timePerEvent": 10.0,
            "sizePerEvent": 2048,
            "maxInputRate": 20000,
            "maxInputEvents": 300,
            "maxInputSize": 300 * 1024 * 1024 * 1024,
            "maxInputFiles": 1000,
            "maxLatency": 345,
            "periodicHarvestInterval": 12,
            "dataType": "express",
            "archivalNode": "ArchivalNode",
            "tapeNode": "TapeNode",
            "diskNode": "DiskNode",
            "blockCloseDelay": 7200,
            "maxMemoryperCore": 2200,
            "dataset_lifetime": 120
        }

        # add Express configuration to a stream
        tier0config.addRepackConfig(self.config, streamName, **options)
        streamConfig = tier0config.retrieveStreamConfig(self.config, streamName)
        self.assertEqual(streamConfig._internal_name, streamName)

    def test_deleteStreamConfig(self):
        # Test with an existing stream
        streamName = "Express"
        options = {
            "versionOverride": {"CMSSW_12_0_0": 1},
            "scenario": "ppEra",
            "data_tiers": ["RAW", "RECO"],
            "global_tag": "GLOBALTAG::All",
            "global_tag_connect": "GTCONNECT",
            "reco_version": "CMSSW_12_0_1",
            "multicore": 8,
            "alca_producers": ["AlcaProducer1", "AlcaProducer2"],
            "write_dqm": True,
            "dqm_sequences": ["DQMSeq1", "DQMSeq2"],
            "proc_ver": 2,
            "timePerEvent": 10.0,
            "sizePerEvent": 2048,
            "maxInputRate": 20000,
            "maxInputEvents": 300,
            "maxInputSize": 300 * 1024 * 1024 * 1024,
            "maxInputFiles": 1000,
            "maxLatency": 345,
            "periodicHarvestInterval": 12,
            "dataType": "express",
            "archivalNode": "ArchivalNode",
            "tapeNode": "TapeNode",
            "diskNode": "DiskNode",
            "blockCloseDelay": 7200,
            "maxMemoryperCore": 2200,
            "dataset_lifetime": 120
        }

        # add Express configuration to a stream
        tier0config.addRepackConfig(self.config, streamName, **options)
        # delete the configuration
        tier0config.deleteStreamConfig(self.config, streamName)

        # Check if the stream configuration has been deleted
        self.assertIsNone(getattr(self.config.Streams, streamName, None))

    def test_retrieveSiteConfig(self):
        
        siteName = "T1_US_FNAL"
        options = {
            "overrideCatalog": "override_catalog.xml",
            "siteLocalConfig": "site_local_config.xml"
        }

        # Add site configuration
        tier0config.addSiteConfig(self.config, siteName, **options)
        siteConfig = tier0config.retrieveSiteConfig(self.config, siteName)
        
        # Check if the returned Config is the correct one
        self.assertEqual(siteConfig._internal_name, siteName)

    def test_deleteSiteConfig(self):
        siteName = "T1_US_FNAL"
        options = {
            "overrideCatalog": "override_catalog.xml",
            "siteLocalConfig": "site_local_config.xml"
        }

        # Add site configuration
        tier0config.addSiteConfig(self.config, siteName, **options)
        tier0config.deleteSiteConfig(self.config, siteName)

        # Check if the site configuration has been deleted
        self.assertIsNone(getattr(self.config.Sites, siteName, None))

    def test_retrieveDatasetConfig(self):
        datasetName = "NewDataset"
        tier0config.addDataset(self.config, datasetName,
                                scenario="Scenario1",
                                do_reco=True,
                                reco_delay=3600,
                                reco_delay_offset=600,
                                proc_version=2,
                                cmssw_version="CMSSW_11_0_1",
                                global_tag="GlobalTag1",
                                reco_split=1000,
                                write_reco=True,
                                write_aod=False,
                                write_miniaod=True,
                                write_nanoaod=True,
                                write_dqm=False,
                                timePerEvent=1,
                                sizePerEvent=1000,
                                global_tag_connect="ConnectStr",
                                archival_node="ArchivalNode",
                                tape_node="TapeNode",
                                raw_tape_node="RawTapeNode",
                                disk_node="DiskNode",
                                disk_node_reco="DiskNodeReco",
                                raw_to_disk=False,
                                aod_to_disk=False,
                                multicore=4,
                                blockCloseDelay=7200,
                                siteWhitelist=["T1_US_FNAL"],
                                alca_producers=["ALCA1", "ALCA2"],
                                physics_skims=["Skim1", "Skim2"],
                                dqm_sequences=["DQM1", "DQM2"],
                                maxMemoryperCore=3000,
                                dataset_lifetime=86400)
        datasetConfig = tier0config.retrieveDatasetConfig(self.config, datasetName)
        self.assertEqual(datasetConfig._internal_name, datasetName)

    def test_retrieveDatasetConfig_fromAddDataset(self):
        # Test with an existing dataset using fromAddDataset flag
        datasetName = "NewDataset"
        tier0config.addDataset(self.config, datasetName,
                                scenario="Scenario1",
                                do_reco=True,
                                reco_delay=3600,
                                reco_delay_offset=600,
                                proc_version=2,
                                cmssw_version="CMSSW_11_0_1",
                                global_tag="GlobalTag1",
                                reco_split=1000,
                                write_reco=True,
                                write_aod=False,
                                write_miniaod=True,
                                write_nanoaod=True,
                                write_dqm=False,
                                timePerEvent=1,
                                sizePerEvent=1000,
                                global_tag_connect="ConnectStr",
                                archival_node="ArchivalNode",
                                tape_node="TapeNode",
                                raw_tape_node="RawTapeNode",
                                disk_node="DiskNode",
                                disk_node_reco="DiskNodeReco",
                                raw_to_disk=False,
                                aod_to_disk=False,
                                multicore=4,
                                blockCloseDelay=7200,
                                siteWhitelist=["T1_US_FNAL"],
                                alca_producers=["ALCA1", "ALCA2"],
                                physics_skims=["Skim1", "Skim2"],
                                dqm_sequences=["DQM1", "DQM2"],
                                maxMemoryperCore=3000,
                                dataset_lifetime=86400)
        with self.assertRaises(RuntimeError):
            tier0config.retrieveDatasetConfig(self.config, datasetName, fromAddDataset=True)

    def test_addDataset(self):
        # Test adding a new dataset with various settings
        datasetName = "NewDataset"
        tier0config.addDataset(self.config, datasetName,
                                scenario="Scenario1",
                                do_reco=True,
                                reco_delay=3600,
                                reco_delay_offset=600,
                                proc_version=2,
                                cmssw_version="CMSSW_11_0_1",
                                global_tag="GlobalTag1",
                                reco_split=1000,
                                write_reco=True,
                                write_aod=False,
                                write_miniaod=True,
                                write_nanoaod=True,
                                write_dqm=False,
                                timePerEvent=1,
                                sizePerEvent=1000,
                                global_tag_connect="ConnectStr",
                                archival_node="ArchivalNode",
                                tape_node="TapeNode",
                                raw_tape_node="RawTapeNode",
                                disk_node="DiskNode",
                                disk_node_reco="DiskNodeReco",
                                raw_to_disk=False,
                                aod_to_disk=False,
                                multicore=4,
                                blockCloseDelay=7200,
                                siteWhitelist=["T1_US_FNAL"],
                                alca_producers=["ALCA1", "ALCA2"],
                                physics_skims=["Skim1", "Skim2"],
                                dqm_sequences=["DQM1", "DQM2"],
                                maxMemoryperCore=3000,
                                dataset_lifetime=86400)

        # Retrieve the added dataset's configuration
        datasetConfig = tier0config.retrieveDatasetConfig(self.config, datasetName)

        # Check if the added settings match the expected values
        self.assertEqual(datasetConfig.Scenario, "Scenario1")
        self.assertTrue(datasetConfig.DoReco)
        self.assertEqual(datasetConfig.RecoDelay, 3600)
        self.assertEqual(datasetConfig.RecoDelayOffset, 600)
        self.assertEqual(datasetConfig.ProcessingVersion, 2)
        self.assertEqual(datasetConfig.CMSSWVersion, "CMSSW_11_0_1")
        self.assertEqual(datasetConfig.GlobalTag, "GlobalTag1")
        self.assertEqual(datasetConfig.RecoSplit, 1000)
        self.assertTrue(datasetConfig.WriteRECO)
        self.assertFalse(datasetConfig.WriteAOD)
        self.assertTrue(datasetConfig.WriteMINIAOD)
        self.assertTrue(datasetConfig.WriteNANOAOD)
        self.assertFalse(datasetConfig.WriteDQM)
        self.assertEqual(datasetConfig.TimePerEvent, 1)
        self.assertEqual(datasetConfig.SizePerEvent, 1000)
        self.assertEqual(datasetConfig.GlobalTagConnect, "ConnectStr")
        self.assertEqual(datasetConfig.ArchivalNode, "ArchivalNode")
        self.assertEqual(datasetConfig.TapeNode, "TapeNode")
        self.assertEqual(datasetConfig.RAWTapeNode, "RawTapeNode")
        self.assertEqual(datasetConfig.DiskNode, "DiskNode")
        self.assertEqual(datasetConfig.DiskNodeReco, "DiskNodeReco")
        self.assertFalse(datasetConfig.RAWtoDisk)
        self.assertFalse(datasetConfig.AODtoDisk)
        self.assertEqual(datasetConfig.Multicore, 4)
        self.assertEqual(datasetConfig.BlockCloseDelay, 7200)
        self.assertEqual(datasetConfig.SiteWhitelist, ["T1_US_FNAL"])
        self.assertEqual(datasetConfig.AlcaSkims, ["ALCA1", "ALCA2"])
        self.assertEqual(datasetConfig.PhysicsSkims, ["Skim1", "Skim2"])
        self.assertEqual(datasetConfig.DqmSequences, ["DQM1", "DQM2"])
        self.assertEqual(datasetConfig.MaxMemoryperCore, 3000)
        self.assertEqual(datasetConfig.datasetLifetime, 86400)

    def test_setAcquisitionEra(self):
        # Set the acquisition era in the configuration
        acquisitionEra = "ERA1"
        tier0config.setAcquisitionEra(self.config, acquisitionEra)

        # Check if the acquisition era is correctly set
        self.assertEqual(self.config.Global.AcquisitionEra, acquisitionEra)

    def test_setScramArch(self):
        # Set the default Scram arch for a specific CMSSW version in the configuration
        cmssw = "CMSSW_11_0_1"
        arch = "slc7_amd64_gcc820"
        tier0config.setScramArch(self.config, cmssw, arch)

        # Check if the Scram arch is correctly set for the given CMSSW version
        self.assertEqual(self.config.Global.ScramArches[cmssw], arch)

    def test_setBaseRequestPriority(self):
        # Set the base request priority in the configuration
        priority = 200000
        tier0config.setBaseRequestPriority(self.config, priority)

        # Check if the base request priority is correctly set
        self.assertEqual(self.config.Global.BaseRequestPriority, priority)

    def test_setDefaultScramArch(self):
        # Set the default Scram arch in the configuration
        arch = "slc7_amd64_gcc820"
        tier0config.setDefaultScramArch(self.config, arch)

        # Check if the default Scram arch is correctly set
        self.assertEqual(self.config.Global.DefaultScramArch, arch)


    def test_setBackfill(self):
        # Set the backfill mode in the configuration
        backfill_mode = 2
        tier0config.setBackfill(self.config, backfill_mode)

        # Check if the backfill mode is correctly set
        self.assertEqual(self.config.Global.Backfill, backfill_mode)

    def test_setProcessingSite(self):
        # Set the processing site in the configuration
        processing_site = "T1_US_FNAL"
        tier0config.setProcessingSite(self.config, processing_site)

        # Check if the processing site is correctly set
        self.assertEqual(self.config.Global.ProcessingSite, processing_site)

    def test_setStorageSite(self):
        # Set the storage site in the configuration
        storage_site = "T2_CH_CERN"
        tier0config.setStorageSite(self.config, storage_site)

        # Check if the storage site is correctly set
        self.assertEqual(self.config.Global.StorageSite, storage_site)

    def test_setStreamerPNN(self):
        # Set the streamer PNN in the configuration
        streamer_pnn = "T0_CH_CERN_Disk"
        tier0config.setStreamerPNN(self.config, streamer_pnn)

        # Check if the streamer PNN is correctly set
        self.assertEqual(self.config.Global.StreamerPNN, streamer_pnn)

    def test_setOverrideCatalog(self):
        # Set the override catalog in the configuration
        override_catalog = "http://example.com/catalog"
        tier0config.setOverrideCatalog(self.config, override_catalog)

        # Check if the override catalog is correctly set
        self.assertEqual(self.config.Global.overrideCatalog, override_catalog)

    def test_setSiteLocalConfig(self):
        # Set the site local config in the configuration
        site_local_config = "/path/to/siteLocalConfig.xml"
        tier0config.setSiteLocalConfig(self.config, site_local_config)

        # Check if the site local config is correctly set
        self.assertEqual(self.config.Global.siteLocalConfig, site_local_config)

    def test_setBulkDataType(self):
        # Set the bulk data type in the configuration
        bulk_data_type = "DATA"
        tier0config.setBulkDataType(self.config, bulk_data_type)

        # Check if the bulk data type is correctly set
        self.assertEqual(self.config.Global.BulkDataType, bulk_data_type)

    def test_setDQMDataTier(self):
        # Set the DQM data tier in the configuration
        dqm_data_tier = "DQMIO"
        tier0config.setDQMDataTier(self.config, dqm_data_tier)

        # Check if the DQM data tier is correctly set
        self.assertEqual(self.config.Global.DQMDataTier, dqm_data_tier)

    def test_setDQMUploadUrl(self):
        # Set the DQM upload URL in the configuration
        dqm_upload_url = "http://example.com/upload"
        tier0config.setDQMUploadUrl(self.config, dqm_upload_url)

        # Check if the DQM upload URL is correctly set
        self.assertEqual(self.config.Global.DQMUploadUrl, dqm_upload_url)


    def test_setPromptCalibrationConfig(self):
        # Set PromptCalibration configuration settings
        alcaHarvestTimeout = 3600
        alcaHarvestCondLFNBase = "/store/unmerged"
        alcaHarvestLumiURL = "https://example.com/lumi"
        conditionUploadTimeout = 600
        dropboxHost = "dropbox.example.com"
        validationMode = "TestMode"

        tier0config.setPromptCalibrationConfig(
                self.config, alcaHarvestTimeout, alcaHarvestCondLFNBase,
                alcaHarvestLumiURL, conditionUploadTimeout, dropboxHost,
                validationMode
        )

        # Check if the PromptCalibration settings are correctly set
        self.assertEqual(self.config.Global.AlcaHarvestTimeout, alcaHarvestTimeout)
        self.assertEqual(self.config.Global.AlcaHarvestCondLFNBase, alcaHarvestCondLFNBase)
        self.assertEqual(self.config.Global.AlcaHarvestLumiURL, alcaHarvestLumiURL)
        self.assertEqual(self.config.Global.ConditionUploadTimeout, conditionUploadTimeout)
        self.assertEqual(self.config.Global.DropboxHost, dropboxHost)
        self.assertEqual(self.config.Global.ValidationMode, validationMode)

    def test_setConfigVersion(self):
        # Set the configuration version
        version = "v1.0.0"
        tier0config.setConfigVersion(self.config, version)

        # Check if the configuration version is correctly set
        self.assertEqual(self.config.Global.Version, version)

    def test_setInjectRuns(self):
        # Set runs to be injected into the Tier0
        injectRuns = [1, 2, 3, 4, 5]
        tier0config.setInjectRuns(self.config, injectRuns)

        # Check if the injected runs are correctly set
        self.assertEqual(self.config.Global.InjectRuns, injectRuns)

    def test_setInjectMinRun(self):
        # Set the lowest run to be injected into the Tier0
        injectMinRun = 10
        tier0config.setInjectMinRun(self.config, injectMinRun)

        # Check if the lowest run is correctly set
        self.assertEqual(self.config.Global.InjectMinRun, injectMinRun)

    def test_setInjectMaxRun(self):
        # Set the highest run to be injected into the Tier0
        injectMaxRun = 100
        tier0config.setInjectMaxRun(self.config, injectMaxRun)

        # Check if the highest run is correctly set
        self.assertEqual(self.config.Global.InjectMaxRun, injectMaxRun)

    def test_setInjectLimit(self):
        # Set the limit of lumis to be injected into the Tier0
        injectLimit = 500
        tier0config.setInjectLimit(self.config, injectLimit)

        # Check if the inject limit is correctly set
        self.assertEqual(self.config.Global.InjectLimit, injectLimit)

    def test_setEnableUniqueWorkflowName(self):
        # Enable unique workflow names in Tier0 replays
        tier0config.setEnableUniqueWorkflowName(self.config)

        # Check if unique workflow names are enabled
        self.assertTrue(self.config.Global.EnableUniqueWorkflowName)

    def test_setDeploymentId(self):
        # Set the deployment ID
        deployment_id = 42
        tier0config.setDeploymentId(self.config, deployment_id)

        # Check if the deployment ID is correctly set
        self.assertEqual(self.config.Global.DeploymentID, deployment_id)

    def test_ignoreStream(self):
        # Ignore a stream in the configuration
        stream_name = "Repack"
        tier0config.ignoreStream(self.config, stream_name)

        # Check if the specified stream is set to be ignored
        stream_config = tier0config.retrieveStreamConfig(self.config, stream_name)
        self.assertEqual(stream_config.ProcessingStyle, "Ignore")

    def test_specifyStreams(self):
        # Specify a list of streamer names to be processed exclusively
        stream_names = ["Express", "PromptReco"]
        tier0config.specifyStreams(self.config, stream_names)

        # Check if the specified stream names are correctly set
        self.assertEqual(self.config.Global.SpecifiedStreamNames, stream_names)

    def test_addRepackConfig(self):
        stream_name = "Repack"
        options = {
            "versionOverride": {"CMSSW_11_0_0": 2},
            "proc_ver": 3,
            "maxSizeSingleLumi": 20 * 1024 * 1024 * 1024,
            "maxSizeMultiLumi": 12 * 1024 * 1024 * 1024,
            "minInputSize": 3.1 * 1024 * 1024 * 1024,
            "maxInputSize": 5 * 1024 * 1024 * 1024,
            "maxEdmSize": 12 * 1024 * 1024 * 1024,
            "maxOverSize": 10 * 1024 * 1024 * 1024,
            "maxInputEvents": 15 * 1000 * 1000,
            "maxInputFiles": 2000,
            "maxLatency": 18 * 3600,
            "blockCloseDelay": 36 * 3600,
            "maxMemory": 3000
        }

        # Add Repack configuration to the stream
        tier0config.addRepackConfig(self.config, stream_name, **options)

        # Check if the Repack configuration settings are correctly set
        repack_config = tier0config.retrieveStreamConfig(self.config, stream_name).Repack
        self.assertEqual(repack_config.ProcessingVersion, options["proc_ver"])
        self.assertEqual(repack_config.MaxSizeSingleLumi, options["maxSizeSingleLumi"])
        self.assertEqual(repack_config.MaxSizeMultiLumi, options["maxSizeMultiLumi"])
        self.assertEqual(repack_config.MinInputSize, options["minInputSize"])
        self.assertEqual(repack_config.MaxInputSize, options["maxInputSize"])
        self.assertEqual(repack_config.MaxEdmSize, options["maxEdmSize"])
        self.assertEqual(repack_config.MaxOverSize, options["maxOverSize"])
        self.assertEqual(repack_config.MaxInputEvents, options["maxInputEvents"])
        self.assertEqual(repack_config.MaxInputFiles, options["maxInputFiles"])
        self.assertEqual(repack_config.MaxLatency, options["maxLatency"])
        self.assertEqual(repack_config.BlockCloseDelay, options["blockCloseDelay"])
        self.assertEqual(repack_config.MaxMemory, options["maxMemory"])

    def test_addExpressConfig(self):
        stream_name = "Express"
        options = {
            "versionOverride": {"CMSSW_12_0_0": 1},
            "scenario": "ppEra",
            "data_tiers": ["RAW", "RECO"],
            "global_tag": "GLOBALTAG::All",
            "global_tag_connect": "GTCONNECT",
            "reco_version": "CMSSW_12_0_1",
            "multicore": 8,
            "alca_producers": ["AlcaProducer1", "AlcaProducer2"],
            "write_dqm": True,
            "dqm_sequences": ["DQMSeq1", "DQMSeq2"],
            "proc_ver": 2,
            "timePerEvent": 10.0,
            "sizePerEvent": 2048,
            "maxInputRate": 20000,
            "maxInputEvents": 300,
            "maxInputSize": 300 * 1024 * 1024 * 1024,
            "maxInputFiles": 1000,
            "maxLatency": 345,
            "periodicHarvestInterval": 12,
            "dataType": "express",
            "archivalNode": "ArchivalNode",
            "tapeNode": "TapeNode",
            "diskNode": "DiskNode",
            "blockCloseDelay": 7200,
            "maxMemoryperCore": 2200,
            "dataset_lifetime": 120
        }

        # Add Express configuration to the stream
        tier0config.addExpressConfig(self.config, stream_name, **options)

        # Check if the Express configuration settings are correctly set
        express_config = tier0config.retrieveStreamConfig(self.config, stream_name)
        self.assertEqual(express_config.ProcessingStyle, "Express")
        self.assertEqual(express_config.VersionOverride, options["versionOverride"])
        express_config = express_config.Express
        self.assertEqual(express_config.Scenario, options["scenario"])
        self.assertEqual(express_config.DataTiers, options["data_tiers"])
        self.assertEqual(express_config.GlobalTag, options["global_tag"])
        self.assertEqual(express_config.GlobalTagConnect, options["global_tag_connect"])
        self.assertEqual(express_config.RecoCMSSWVersion, options["reco_version"])
        self.assertEqual(express_config.Multicore, options["multicore"])
        self.assertEqual(express_config.AlcaSkims, options["alca_producers"])
        self.assertEqual(express_config.WriteDQM, options["write_dqm"])
        self.assertEqual(express_config.DqmSequences, options["dqm_sequences"])
        self.assertEqual(express_config.ProcessingVersion, options["proc_ver"])
        self.assertEqual(express_config.TimePerEvent, options["timePerEvent"])
        self.assertEqual(express_config.SizePerEvent, options["sizePerEvent"])
        self.assertEqual(express_config.MaxInputRate, options["maxInputRate"])
        self.assertEqual(express_config.MaxInputEvents, options["maxInputEvents"])
        self.assertEqual(express_config.MaxInputSize, options["maxInputSize"])
        self.assertEqual(express_config.MaxInputFiles, options["maxInputFiles"])
        self.assertEqual(express_config.MaxLatency, options["maxLatency"])
        self.assertEqual(express_config.PeriodicHarvestInterval, options["periodicHarvestInterval"])
        self.assertEqual(express_config.DataType, options["dataType"])
        self.assertEqual(express_config.ArchivalNode, options["archivalNode"])
        self.assertEqual(express_config.TapeNode, options["tapeNode"])
        self.assertEqual(express_config.DiskNode, options["diskNode"])
        self.assertEqual(express_config.BlockCloseDelay, options["blockCloseDelay"])
        self.assertEqual(express_config.MaxMemoryperCore, options["maxMemoryperCore"])
        self.assertEqual(express_config.datasetLifetime, options["dataset_lifetime"])

    def test_addSiteConfig(self):
        site_name = "SiteName"
        options = {
            "overrideCatalog": "override_catalog.xml",
            "siteLocalConfig": "site_local_config.xml"
        }

        # Add site configuration
        tier0config.addSiteConfig(self.config, site_name, **options)

        # Check if the site configuration settings are correctly set
        site_config = tier0config.retrieveSiteConfig(self.config, site_name)
        self.assertEqual(site_config.OverrideCatalog, options["overrideCatalog"])
        self.assertEqual(site_config.SiteLocalConfig, options["siteLocalConfig"])

    def test_addRegistrationConfig(self):
        stream_name = "StreamName"
        options = {
            "primds": "PrimaryDataset",
            "data_tier": "DATA",
            "acq_era": "ERA",
            "proc_version": "1",
            "proc_string": "PROCSTRING",
            "versionOverride": {"CMSSW_12_0_0": 1}
        }
        streamConfig = tier0config.retrieveStreamConfig(self.config, stream_name)
        streamConfig.ProcessingStyle = "Convert"


        # Add registration configuration to the stream
        tier0config.addRegistrationConfig(self.config, stream_name, **options)

        # Check if the registration configuration settings are correctly set
        stream_config = tier0config.retrieveStreamConfig(self.config, stream_name)
        self.assertEqual(stream_config.ProcessingStyle, "RegisterAndConvert")
        self.assertEqual(stream_config.VersionOverride, options["versionOverride"])
        register_config = stream_config.Register
        self.assertEqual(register_config.PrimaryDataset, options["primds"])
        self.assertEqual(register_config.DataTier, options["data_tier"])
        self.assertEqual(register_config.ProcessedDataset, "ERA-PROCSTRING-1")

    def test_addConversionConfig(self):
        stream_name = "StreamName"
        options = {
            "primds": "PrimaryDataset",
            "data_tier": "DATA",
            "conv_type": "ConversionType",
            "acq_era": "ERA",
            "proc_version": "1",
            "proc_string": "PROCSTRING",
            "versionOverride": {"CMSSW_12_0_0": 1}
        }

        stream_config = tier0config.retrieveStreamConfig(self.config, stream_name)
        stream_config.ProcessingStyle = "Register"

        # Add conversion configuration to the stream
        tier0config.addConversionConfig(self.config, stream_name, **options)

        # Check if the conversion configuration settings are correctly set
        stream_config = tier0config.retrieveStreamConfig(self.config, stream_name)
        self.assertEqual(stream_config.ProcessingStyle, "RegisterAndConvert")
        self.assertEqual(stream_config.VersionOverride, options["versionOverride"])
        convert_config = stream_config.Convert
        self.assertEqual(convert_config.PrimaryDataset, options["primds"])
        self.assertEqual(convert_config.DataTier, options["data_tier"])
        self.assertEqual(convert_config.Type, options["conv_type"])
        self.assertEqual(convert_config.AcqEra, options["acq_era"])
        self.assertEqual(convert_config.ProcVers, options["proc_version"])
        self.assertEqual(convert_config.ProcString, options["proc_string"])
        self.assertEqual(convert_config.ProcessedDataset, "ERA-PROCSTRING-1")

if __name__ == '__main__':
    unittest.main()