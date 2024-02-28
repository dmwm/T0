import unittest
import T0.RunConfig.Tier0Config as tier0config
from T0.RunConfig import RunConfigAPI


class TestRetrieveStreamConfig(unittest.TestCase):

    def setUp(self):
        self.config = tier0config.createTier0Config()
        self.hltconfig = None
        
    def test_parseHLTConfig(self):
        # Check keys for bindCombinations.
        if self.hltconfig is None:
            self.hltconfig={'mapping':{'stream1':{'dataset1':['path1','path2']},'stream2':{'dataset2':['path3','path4']}}}
        bindsCombination=RunConfigAPI.parseHLTConfig(176161,self.hltconfig)
        
        for mapping in ['Stream','Dataset','StreamDataset','Trigger','DatasetTrigger']:
            with self.subTest(mapping=mapping):
                self.assertIn(mapping,bindsCombination)
                self.assertNotEqual(bindsCombination[mapping],[])
                
        self.assertIn(bindsCombination['Stream'][0],'STREAM')
        self.assertIn(bindsCombination['Dataset'][0],'PRIMDS')
        self.assertIn(bindsCombination['StreamDataset'][0],'RUN')
        self.assertIn(bindsCombination['StreamDataset'][0],'PRIMDS')
        self.assertIn(bindsCombination['StreamDataset'][0],'STREAM')
        self.assertIn(bindsCombination['Trigger'][0],'TRIG')
        self.assertIn(bindsCombination['DatasetTrigger'][0],'RUN')
        self.assertIn(bindsCombination['DatasetTrigger'][0],'TRIG')
        self.assertIn(bindsCombination['DatasetTrigger'][0],'PRIMDS')    
        
    def test_getCustodialSite(self):
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
        bindsStorageNode = []
        custodialSites,nonCustodialSites,bindsStorageNode = RunConfigAPI.getCustodialSite(datasetConfig,bindsStorageNode,isExpress=False)
        self.assertIn(bindsStorageNode,{"Node":"ArchivalNode"})
        self.assertIn(custodialSites,"ArchivalNode")
        self.assertIn(nonCustodialSites,"DiskNode")

if __name__ == '__main__':
    unittest.main()