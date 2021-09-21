#!/usr/bin/env python
"""
_Tier0Feeder_t_

Testing the Tier0Feeder code

"""

import unittest
import threading
import logging
import time
import os

from WMQuality.TestInit import TestInit
from WMCore.DAOFactory import DAOFactory
from WMCore.Database.DBFactory import DBFactory
from WMCore.Configuration import loadConfigurationFile
from WMCore.Services.UUIDLib import makeUUID
from WMCore.Services.RequestDB.RequestDBWriter import RequestDBWriter

from T0.RunConfig import RunConfigAPI
from T0.RunLumiCloseout import RunLumiCloseoutAPI
from T0.ConditionUpload import ConditionUploadAPI
from T0.StorageManager import StorageManagerAPI

class Tier0FeederTest(unittest.TestCase):
    """
    _Tier0FeederTest_

    Testing the Tier0Feeder code
    """

    def setUp(self):
        """
        _setUp_

        """
        self.testInit = TestInit(__file__)
        self.testInit.setLogging()
        self.testInit.setDatabaseConnection(destroyAllDatabase=True)
        self.p5id=1
        self.testInit.setSchema(customModules = ["WMComponent.DBS3Buffer", "T0.WMBS"])

        self.testDir  = self.testInit.generateWorkDir()

        self.hltkey = "/cdaq/physics/Run2011/3e33/v2.1/HLT/V2"
        self.hltConfig = None
        self.dqmUploadProxy = None
        self.dbInterfaceStorageManager = None
        self.getExpressReadyRunsDAO = None

        if 'WMAGENT_CONFIG' in os.environ:

            wmAgentConfig = loadConfigurationFile(os.environ["WMAGENT_CONFIG"])

            self.dqmUploadProxy = getattr(wmAgentConfig.Tier0Feeder, "dqmUploadProxy", None)

            self.localRequestCouchDB = RequestDBWriter(wmAgentConfig.AnalyticsDataCollector.localT0RequestDBURL,
                                                       couchapp = wmAgentConfig.AnalyticsDataCollector.RequestCouchApp)

            if hasattr(wmAgentConfig, "HLTConfDatabase"):

                connectUrl = getattr(wmAgentConfig.HLTConfDatabase, "connectUrl", None)

                dbFactory = DBFactory(logging, dburl = connectUrl, options = {})
                dbInterface = dbFactory.connect()
                #print(dbInterface, "this is the dbinterface")

                daoFactory = DAOFactory(package = "T0.WMBS",
                                        logger = logging,
                                        dbinterface = dbInterface)
                self.dbInterface = dbInterface
                getHLTConfigDAO = daoFactory(classname = "RunConfig.GetHLTConfig")
                self.hltConfig = getHLTConfigDAO.execute(self.hltkey, transaction = False)

                if self.hltConfig['process'] == None or len(self.hltConfig['mapping']) == 0:
                    raise RuntimeError("HLTConfDB query returned no process or mapping")

            else:
                print("Your config is missing the HLTConfDatabase section")
                print("Using reference HLT config instead")

            if hasattr(wmAgentConfig, "StorageManagerDatabase"):

                connectUrl = getattr(wmAgentConfig.StorageManagerDatabase, "connectUrl", None)

                dbFactory = DBFactory(logging, dburl = connectUrl, options = {})
                self.dbInterfaceStorageManager = dbFactory.connect()

            else:
                print("Did not connect to Storagemanagerdatabase")
            if hasattr(wmAgentConfig, "PopConLogDatabase"):

                connectUrl = getattr(wmAgentConfig.PopConLogDatabase, "connectUrl", None)

                dbFactory = DBFactory(logging, dburl = connectUrl, options = {})
                dbInterface = dbFactory.connect()

                daoFactory = DAOFactory(package = "T0.WMBS",
                                        logger = logging,
                                        dbinterface = dbInterface)
                self.getExpressReadyRunsDAO = daoFactory(classname = "Tier0Feeder.GetExpressReadyRuns")
            else:
                print("Did not connect to popconlogdatabase")
        else:
            print("You do not have WMAGENT_CONFIG in your environment")
            print("Using reference HLT config instead")

        myThread = threading.currentThread()
        daoFactory = DAOFactory(package = "T0.WMBS",
                                logger = logging,
                                dbinterface = myThread.dbi)

        self.dbInterfaceSMNotify = None
       
        insertCMSSVersionDAO = daoFactory(classname = "RunConfig.InsertCMSSWVersion")
        insertCMSSVersionDAO.execute(binds = { 'VERSION' : "CMSSW_4_2_7" },
                                     transaction = False)

        insertStreamDAO = daoFactory(classname = "RunConfig.InsertStream")
        insertStreamDAO.execute(binds = { 'STREAM' : "A" },
                                transaction = False)
        insertStreamDAO.execute(binds = { 'STREAM' : "Express" },
                                transaction = False)
        insertStreamDAO.execute(binds = { 'STREAM' : "HLTMON" },
                                transaction = False)

        self.tier0Config = loadConfigurationFile("ExampleConfig.py")

        self.insertLocation(self.tier0Config.Global.StreamerPNN)

        self.referenceMapping = {}
        self.referenceMapping['A'] = {}
        self.referenceMapping['A']['BTag'] = []
        self.referenceMapping['A']['BTag'].append("HLT_BTagMu_DiJet110_Mu5_v10")
        self.referenceMapping['A']['BTag'].append("HLT_BTagMu_DiJet20_Mu5_v10")
        self.referenceMapping['A']['BTag'].append("HLT_BTagMu_DiJet40_Mu5_v10")
        self.referenceMapping['A']['BTag'].append("HLT_BTagMu_DiJet70_Mu5_v10")
        self.referenceMapping['A']['Commissioning'] = []
        self.referenceMapping['A']['Commissioning'].append("HLT_Activity_Ecal_SC7_v8")
        self.referenceMapping['A']['Commissioning'].append("HLT_BeamGas_BSC_v5")
        self.referenceMapping['A']['Commissioning'].append("HLT_BeamGas_HF_v6")
        self.referenceMapping['A']['Commissioning'].append("HLT_IsoTrackHB_v7")
        self.referenceMapping['A']['Commissioning'].append("HLT_IsoTrackHE_v8")
        self.referenceMapping['A']['Commissioning'].append("HLT_L1SingleEG12_v3")
        self.referenceMapping['A']['Commissioning'].append("HLT_L1SingleEG5_v3")
        self.referenceMapping['A']['Commissioning'].append("HLT_L1SingleJet16_v4")
        self.referenceMapping['A']['Commissioning'].append("HLT_L1SingleJet36_v4")
        self.referenceMapping['A']['Commissioning'].append("HLT_L1SingleMuOpen_DT_v4")
        self.referenceMapping['A']['Commissioning'].append("HLT_L1SingleMuOpen_v4")
        self.referenceMapping['A']['Commissioning'].append("HLT_L1_Interbunch_BSC_v3")
        self.referenceMapping['A']['Commissioning'].append("HLT_L1_PreCollisions_v3")
        self.referenceMapping['A']['Commissioning'].append("HLT_Mu5_TkMu0_OST_Jpsi_Tight_B5Q7_v9")
        self.referenceMapping['A']['Cosmics'] = []
        self.referenceMapping['A']['Cosmics'].append("HLT_BeamHalo_v6")
        self.referenceMapping['A']['Cosmics'].append("HLT_L1SingleMuOpen_AntiBPTX_v3")
        self.referenceMapping['A']['Cosmics'].append("HLT_L1TrackerCosmics_v4")
        self.referenceMapping['A']['Cosmics'].append("HLT_RegionalCosmicTracking_v7")
        self.referenceMapping['A']['DoubleElectron'] = []
        self.referenceMapping['A']['DoubleElectron'].append("HLT_DoubleEle10_CaloIdL_TrkIdVL_Ele10_CaloIdT_TrkIdVL_v3")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele17_CaloIdL_CaloIsoVL_v8")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v8")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele17_CaloIdVT_CaloIsoVT_TrkIdT_TrkIsoVT_Ele8_Mass30_v7")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele17_CaloIdVT_CaloIsoVT_TrkIdT_TrkIsoVT_SC8_Mass30_v8")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele22_CaloIdL_CaloIsoVL_Ele15_HFT_v1")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele32_CaloIdT_CaloIsoT_TrkIdT_TrkIsoT_Ele17_v1")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele32_CaloIdT_CaloIsoT_TrkIdT_TrkIsoT_SC17_v6")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele8_CaloIdL_CaloIsoVL_Jet40_v8")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele8_CaloIdL_CaloIsoVL_v8")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele8_CaloIdL_TrkIdVL_v8")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v6")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Ele8_v8")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_Photon20_CaloIdVT_IsoT_Ele8_CaloIdL_CaloIsoVL_v9")
        self.referenceMapping['A']['DoubleElectron'].append("HLT_TripleEle10_CaloIdL_TrkIdVL_v9")
        self.referenceMapping['A']['DoubleMu'] = []
        self.referenceMapping['A']['DoubleMu'].append("HLT_DoubleMu3_v10")
        self.referenceMapping['A']['DoubleMu'].append("HLT_DoubleMu45_v6")
        self.referenceMapping['A']['DoubleMu'].append("HLT_DoubleMu5_Acoplanarity03_v6")
        self.referenceMapping['A']['DoubleMu'].append("HLT_DoubleMu5_IsoMu5_v8")
        self.referenceMapping['A']['DoubleMu'].append("HLT_DoubleMu5_v1")
        self.referenceMapping['A']['DoubleMu'].append("HLT_DoubleMu6_Acoplanarity03_v1")
        self.referenceMapping['A']['DoubleMu'].append("HLT_DoubleMu6_v8")
        self.referenceMapping['A']['DoubleMu'].append("HLT_DoubleMu7_v8")
        self.referenceMapping['A']['DoubleMu'].append("HLT_L1DoubleMu0_v4")
        self.referenceMapping['A']['DoubleMu'].append("HLT_L2DoubleMu0_v7")
        self.referenceMapping['A']['DoubleMu'].append("HLT_L2DoubleMu23_NoVertex_v7")
        self.referenceMapping['A']['DoubleMu'].append("HLT_L2DoubleMu30_NoVertex_v3")
        self.referenceMapping['A']['DoubleMu'].append("HLT_Mu13_Mu8_v7")
        self.referenceMapping['A']['DoubleMu'].append("HLT_Mu17_Mu8_v7")
        self.referenceMapping['A']['DoubleMu'].append("HLT_Mu8_Jet40_v10")
        self.referenceMapping['A']['DoubleMu'].append("HLT_TripleMu5_v9")
        self.referenceMapping['A']['ElectronHad'] = []
        self.referenceMapping['A']['ElectronHad'].append("HLT_DoubleEle8_CaloIdT_TrkIdVL_HT150_v6")
        self.referenceMapping['A']['ElectronHad'].append("HLT_DoubleEle8_CaloIdT_TrkIdVL_Mass4_HT150_v3")
        self.referenceMapping['A']['ElectronHad'].append("HLT_DoubleEle8_CaloIdT_TrkIdVL_v3")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele12_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_R005_MR200_v1")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele12_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_R025_MR200_v1")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele12_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_R029_MR200_v1")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele15_CaloIdT_CaloIsoVL_TrkIdT_TrkIsoVL_HT250_PFMHT25_v4")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele15_CaloIdT_CaloIsoVL_TrkIdT_TrkIsoVL_HT250_PFMHT40_v1")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele15_CaloIdT_CaloIsoVL_TrkIdT_TrkIsoVL_v2")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele20_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_Jet35_Jet25_Deta3_Jet20_v2")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralJet30_BTagIP_v5")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralJet30_v5")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_DiCentralJet30_v5")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_QuadCentralJet30_v5")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralJet30_v5")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele25_CaloIdVT_TrkIdT_CentralJet30_BTagIP_v9")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele25_CaloIdVT_TrkIdT_CentralJet30_v9")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele25_CaloIdVT_TrkIdT_DiCentralJet30_v8")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele25_CaloIdVT_TrkIdT_QuadCentralJet30_v5")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele25_CaloIdVT_TrkIdT_TriCentralJet30_v8")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralJet30_CentralJet25_PFMHT20_v2")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralJet30_CentralJet25_v1")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_Jet35_Jet25_Deta3_Jet20_v1")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele27_CaloIdVT_TrkIdT_CentralJet30_CentralJet25_v1")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele27_CaloIdVT_TrkIdT_Jet35_Jet25_Deta3_Jet20_v1")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele30_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_DiCentralJet30_PFMHT25_v1")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele30_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_Jet35_Jet25_Deta3p5_Jet25_v1")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele8_CaloIdT_TrkIdT_DiJet30_v5")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele8_CaloIdT_TrkIdT_QuadJet30_v5")
        self.referenceMapping['A']['ElectronHad'].append("HLT_Ele8_CaloIdT_TrkIdT_TriJet30_v5")
        self.referenceMapping['A']['ElectronHad'].append("HLT_HT200_DoubleEle5_CaloIdVL_MassJPsi_v3")
        self.referenceMapping['A']['ElectronHad'].append("HLT_HT300_Ele5_CaloIdVL_CaloIsoVL_TrkIdVL_TrkIsoVL_PFMHT40_v6")
        self.referenceMapping['A']['ElectronHad'].append("HLT_HT350_Ele30_CaloIdT_TrkIdT_v1")
        self.referenceMapping['A']['ElectronHad'].append("HLT_HT350_Ele5_CaloIdVL_CaloIsoVL_TrkIdVL_TrkIsoVL_PFMHT45_v6")
        self.referenceMapping['A']['ElectronHad'].append("HLT_HT400_Ele60_CaloIdT_TrkIdT_v1")
        self.referenceMapping['A']['FEDMonitor'] = []
        self.referenceMapping['A']['FEDMonitor'].append("HLT_DTErrors_v2")
        self.referenceMapping['A']['HT'] = []
        self.referenceMapping['A']['HT'].append("HLT_DiJet130_PT130_v6")
        self.referenceMapping['A']['HT'].append("HLT_DiJet160_PT160_v6")
        self.referenceMapping['A']['HT'].append("HLT_FatJetMass750_DR1p1_Deta2p0_v2")
        self.referenceMapping['A']['HT'].append("HLT_FatJetMass850_DR1p1_Deta2p0_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT150_v8")
        self.referenceMapping['A']['HT'].append("HLT_HT2000_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT200_AlphaT0p55_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT200_v8")
        self.referenceMapping['A']['HT'].append("HLT_HT250_AlphaT0p53_v6")
        self.referenceMapping['A']['HT'].append("HLT_HT250_AlphaT0p55_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT250_DoubleDisplacedJet60_PromptTrack_v6")
        self.referenceMapping['A']['HT'].append("HLT_HT250_DoubleDisplacedJet60_v8")
        self.referenceMapping['A']['HT'].append("HLT_HT250_MHT100_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT250_MHT90_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT250_v8")
        self.referenceMapping['A']['HT'].append("HLT_HT300_AlphaT0p53_v6")
        self.referenceMapping['A']['HT'].append("HLT_HT300_AlphaT0p54_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT300_CentralJet30_BTagIP_PFMHT55_v8")
        self.referenceMapping['A']['HT'].append("HLT_HT300_CentralJet30_BTagIP_PFMHT65_v1")
        self.referenceMapping['A']['HT'].append("HLT_HT300_CentralJet30_BTagIP_v7")
        self.referenceMapping['A']['HT'].append("HLT_HT300_MHT80_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT300_MHT90_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT300_PFMHT55_v8")
        self.referenceMapping['A']['HT'].append("HLT_HT300_PFMHT65_v1")
        self.referenceMapping['A']['HT'].append("HLT_HT300_v9")
        self.referenceMapping['A']['HT'].append("HLT_HT350_AlphaT0p52_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT350_AlphaT0p53_v7")
        self.referenceMapping['A']['HT'].append("HLT_HT350_MHT70_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT350_MHT80_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT350_MHT90_v1")
        self.referenceMapping['A']['HT'].append("HLT_HT350_v8")
        self.referenceMapping['A']['HT'].append("HLT_HT400_AlphaT0p51_v7")
        self.referenceMapping['A']['HT'].append("HLT_HT400_AlphaT0p52_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT400_MHT80_v1")
        self.referenceMapping['A']['HT'].append("HLT_HT400_v8")
        self.referenceMapping['A']['HT'].append("HLT_HT450_AlphaT0p51_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT450_AlphaT0p52_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT450_v8")
        self.referenceMapping['A']['HT'].append("HLT_HT500_JetPt60_DPhi2p94_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT500_v8")
        self.referenceMapping['A']['HT'].append("HLT_HT550_JetPt60_DPhi2p94_v2")
        self.referenceMapping['A']['HT'].append("HLT_HT550_v8")
        self.referenceMapping['A']['HT'].append("HLT_HT600_JetPt60_DPhi2p94_v1")
        self.referenceMapping['A']['HT'].append("HLT_HT600_v1")
        self.referenceMapping['A']['HT'].append("HLT_HT650_v1")
        self.referenceMapping['A']['HT'].append("HLT_R014_MR150_v7")
        self.referenceMapping['A']['HT'].append("HLT_R020_MR150_v7")
        self.referenceMapping['A']['HT'].append("HLT_R020_MR550_v7")
        self.referenceMapping['A']['HT'].append("HLT_R023_MR550_v3")
        self.referenceMapping['A']['HT'].append("HLT_R025_MR150_v7")
        self.referenceMapping['A']['HT'].append("HLT_R025_MR450_v7")
        self.referenceMapping['A']['HT'].append("HLT_R029_MR450_v3")
        self.referenceMapping['A']['HT'].append("HLT_R033_MR350_v7")
        self.referenceMapping['A']['HT'].append("HLT_R036_MR350_v3")
        self.referenceMapping['A']['HT'].append("HLT_R038_MR250_v7")
        self.referenceMapping['A']['HT'].append("HLT_R042_MR250_v3")
        self.referenceMapping['A']['HcalHPDNoise'] = []
        self.referenceMapping['A']['HcalHPDNoise'].append("HLT_GlobalRunHPDNoise_v5")
        self.referenceMapping['A']['HcalHPDNoise'].append("HLT_L1Tech_HBHEHO_totalOR_v3")
        self.referenceMapping['A']['HcalHPDNoise'].append("HLT_L1Tech_HCAL_HF_single_channel_v1")
        self.referenceMapping['A']['HcalNZS'] = []
        self.referenceMapping['A']['HcalNZS'].append("HLT_HcalNZS_v7")
        self.referenceMapping['A']['HcalNZS'].append("HLT_HcalPhiSym_v8")
        self.referenceMapping['A']['HighPileUp'] = []
        self.referenceMapping['A']['HighPileUp'].append("HLT_60Jet10_v1")
        self.referenceMapping['A']['HighPileUp'].append("HLT_70Jet10_v1")
        self.referenceMapping['A']['HighPileUp'].append("HLT_70Jet13_v1")
        self.referenceMapping['A']['Jet'] = []
        self.referenceMapping['A']['Jet'].append("HLT_DiJetAve110_v6")
        self.referenceMapping['A']['Jet'].append("HLT_DiJetAve190_v6")
        self.referenceMapping['A']['Jet'].append("HLT_DiJetAve240_v6")
        self.referenceMapping['A']['Jet'].append("HLT_DiJetAve300_v6")
        self.referenceMapping['A']['Jet'].append("HLT_DiJetAve30_v6")
        self.referenceMapping['A']['Jet'].append("HLT_DiJetAve370_v6")
        self.referenceMapping['A']['Jet'].append("HLT_DiJetAve60_v6")
        self.referenceMapping['A']['Jet'].append("HLT_Jet110_v6")
        self.referenceMapping['A']['Jet'].append("HLT_Jet190_v6")
        self.referenceMapping['A']['Jet'].append("HLT_Jet240_CentralJet30_BTagIP_v3")
        self.referenceMapping['A']['Jet'].append("HLT_Jet240_v6")
        self.referenceMapping['A']['Jet'].append("HLT_Jet270_CentralJet30_BTagIP_v3")
        self.referenceMapping['A']['Jet'].append("HLT_Jet300_v5")
        self.referenceMapping['A']['Jet'].append("HLT_Jet30_v6")
        self.referenceMapping['A']['Jet'].append("HLT_Jet370_NoJetID_v6")
        self.referenceMapping['A']['Jet'].append("HLT_Jet370_v6")
        self.referenceMapping['A']['Jet'].append("HLT_Jet60_v6")
        self.referenceMapping['A']['Jet'].append("HLT_Jet800_v1")
        self.referenceMapping['A']['LogMonitor'] = []
        self.referenceMapping['A']['LogMonitor'].append("HLT_LogMonitor_v1")
        self.referenceMapping['A']['MET'] = []
        self.referenceMapping['A']['MET'].append("HLT_CentralJet80_MET100_v7")
        self.referenceMapping['A']['MET'].append("HLT_CentralJet80_MET160_v7")
        self.referenceMapping['A']['MET'].append("HLT_CentralJet80_MET65_v7")
        self.referenceMapping['A']['MET'].append("HLT_CentralJet80_MET80_v6")
        self.referenceMapping['A']['MET'].append("HLT_DiCentralJet20_BTagIP_MET65_v7")
        self.referenceMapping['A']['MET'].append("HLT_DiCentralJet20_MET100_HBHENoiseFiltered_v1")
        self.referenceMapping['A']['MET'].append("HLT_DiCentralJet20_MET80_v5")
        self.referenceMapping['A']['MET'].append("HLT_DiJet60_MET45_v7")
        self.referenceMapping['A']['MET'].append("HLT_L2Mu60_1Hit_MET40_v5")
        self.referenceMapping['A']['MET'].append("HLT_L2Mu60_1Hit_MET60_v5")
        self.referenceMapping['A']['MET'].append("HLT_MET100_HBHENoiseFiltered_v6")
        self.referenceMapping['A']['MET'].append("HLT_MET100_v7")
        self.referenceMapping['A']['MET'].append("HLT_MET120_HBHENoiseFiltered_v6")
        self.referenceMapping['A']['MET'].append("HLT_MET120_v7")
        self.referenceMapping['A']['MET'].append("HLT_MET200_HBHENoiseFiltered_v6")
        self.referenceMapping['A']['MET'].append("HLT_MET200_v7")
        self.referenceMapping['A']['MET'].append("HLT_MET400_v2")
        self.referenceMapping['A']['MET'].append("HLT_MET65_HBHENoiseFiltered_v5")
        self.referenceMapping['A']['MET'].append("HLT_MET65_v4")
        self.referenceMapping['A']['MET'].append("HLT_PFMHT150_v12")
        self.referenceMapping['A']['MinimumBias'] = []
        self.referenceMapping['A']['MinimumBias'].append("HLT_JetE30_NoBPTX3BX_NoHalo_v8")
        self.referenceMapping['A']['MinimumBias'].append("HLT_JetE30_NoBPTX_NoHalo_v8")
        self.referenceMapping['A']['MinimumBias'].append("HLT_JetE30_NoBPTX_v6")
        self.referenceMapping['A']['MinimumBias'].append("HLT_JetE50_NoBPTX3BX_NoHalo_v3")
        self.referenceMapping['A']['MinimumBias'].append("HLT_Physics_v2")
        self.referenceMapping['A']['MinimumBias'].append("HLT_PixelTracks_Multiplicity100_v7")
        self.referenceMapping['A']['MinimumBias'].append("HLT_PixelTracks_Multiplicity80_v7")
        self.referenceMapping['A']['MinimumBias'].append("HLT_Random_v1")
        self.referenceMapping['A']['MinimumBias'].append("HLT_ZeroBias_v4")
        self.referenceMapping['A']['MuEG'] = []
        self.referenceMapping['A']['MuEG'].append("HLT_DoubleMu5_Ele8_CaloIdL_TrkIdVL_v10")
        self.referenceMapping['A']['MuEG'].append("HLT_DoubleMu5_Ele8_CaloIdT_TrkIdVL_v4")
        self.referenceMapping['A']['MuEG'].append("HLT_Mu15_DoublePhoton15_CaloIdL_v10")
        self.referenceMapping['A']['MuEG'].append("HLT_Mu15_Photon20_CaloIdL_v10")
        self.referenceMapping['A']['MuEG'].append("HLT_Mu17_Ele8_CaloIdL_v9")
        self.referenceMapping['A']['MuEG'].append("HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_v4")
        self.referenceMapping['A']['MuEG'].append("HLT_Mu5_DoubleEle8_CaloIdT_TrkIdVL_v4")
        self.referenceMapping['A']['MuEG'].append("HLT_Mu5_Ele8_CaloIdT_CaloIsoVL_v1")
        self.referenceMapping['A']['MuEG'].append("HLT_Mu5_Ele8_CaloIdT_TrkIdVL_Ele8_CaloIdL_TrkIdVL_v4")
        self.referenceMapping['A']['MuEG'].append("HLT_Mu8_Ele17_CaloIdL_v9")
        self.referenceMapping['A']['MuEG'].append("HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_v4")
        self.referenceMapping['A']['MuEG'].append("HLT_Mu8_Photon20_CaloIdVT_IsoT_v9")
        self.referenceMapping['A']['MuHad'] = []
        self.referenceMapping['A']['MuHad'].append("HLT_DoubleMu5_HT150_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_DoubleMu5_Mass4_HT150_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_HT250_Mu15_PFMHT40_v4")
        self.referenceMapping['A']['MuHad'].append("HLT_HT300_Mu15_PFMHT40_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_HT300_Mu5_PFMHT40_v8")
        self.referenceMapping['A']['MuHad'].append("HLT_HT350_Mu5_PFMHT45_v8")
        self.referenceMapping['A']['MuHad'].append("HLT_IsoMu17_eta2p1_CentralJet30_BTagIP_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_IsoMu17_eta2p1_CentralJet30_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_IsoMu17_eta2p1_DiCentralJet30_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_IsoMu17_eta2p1_QuadCentralJet30_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_IsoMu17_eta2p1_TriCentralJet30_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_IsoMu20_DiCentralJet34_v3")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu10_R005_MR200_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu10_R025_MR200_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu10_R029_MR200_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu12_eta2p1_DiCentralJet20_BTagIP3D1stTrack_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu12_eta2p1_DiCentralJet20_DiBTagIP3D1stTrack_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu12_eta2p1_DiCentralJet30_BTagIP3D_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu17_eta2p1_CentralJet30_BTagIP_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu17_eta2p1_CentralJet30_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu17_eta2p1_DiCentralJet30_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu17_eta2p1_QuadCentralJet30_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu17_eta2p1_TriCentralJet30_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu40_HT200_v4")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu5_DiJet30_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu5_Ele8_CaloIdT_TrkIdVL_HT150_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu5_Ele8_CaloIdT_TrkIdVL_Mass4_HT150_v6")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu5_QuadJet30_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu5_TriJet30_v1")
        self.referenceMapping['A']['MuHad'].append("HLT_Mu60_HT200_v1")
        self.referenceMapping['A']['MuOnia'] = []
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon0_Jpsi_Muon_v7")
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon0_Jpsi_NoVertexing_v3")
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon0_Jpsi_v6")
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon0_Upsilon_Muon_v7")
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon0_Upsilon_v6")
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon10_Jpsi_Barrel_v6")
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon11_PsiPrime_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon13_Jpsi_Barrel_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon6_LowMass_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon7_Upsilon_Barrel_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon9_PsiPrime_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_Dimuon9_Upsilon_Barrel_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_DoubleMu4_Dimuon4_Bs_Barrel_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_DoubleMu4_Dimuon6_Bs_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_DoubleMu4_Jpsi_Displaced_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_DoubleMu4p5_LowMass_Displaced_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_DoubleMu5_Jpsi_Displaced_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_DoubleMu5_LowMass_Displaced_v1")
        self.referenceMapping['A']['MuOnia'].append("HLT_Mu5_L2Mu2_Jpsi_v9")
        self.referenceMapping['A']['MuOnia'].append("HLT_Mu5_Track2_Jpsi_v9")
        self.referenceMapping['A']['MuOnia'].append("HLT_Mu7_Track7_Jpsi_v10")
        self.referenceMapping['A']['MultiJet'] = []
        self.referenceMapping['A']['MultiJet'].append("HLT_CentralJet46_CentralJet38_CentralJet20_DiBTagIP3D_v1")
        self.referenceMapping['A']['MultiJet'].append("HLT_CentralJet46_CentralJet38_DiBTagIP3D_v3")
        self.referenceMapping['A']['MultiJet'].append("HLT_CentralJet60_CentralJet53_DiBTagIP3D_v2")
        self.referenceMapping['A']['MultiJet'].append("HLT_DiCentralJet36_BTagIP3DLoose_v1")
        self.referenceMapping['A']['MultiJet'].append("HLT_DoubleJet30_ForwardBackward_v7")
        self.referenceMapping['A']['MultiJet'].append("HLT_DoubleJet60_ForwardBackward_v7")
        self.referenceMapping['A']['MultiJet'].append("HLT_DoubleJet70_ForwardBackward_v7")
        self.referenceMapping['A']['MultiJet'].append("HLT_DoubleJet80_ForwardBackward_v7")
        self.referenceMapping['A']['MultiJet'].append("HLT_EightJet120_v1")
        self.referenceMapping['A']['MultiJet'].append("HLT_ExclDiJet60_HFAND_v6")
        self.referenceMapping['A']['MultiJet'].append("HLT_ExclDiJet60_HFOR_v6")
        self.referenceMapping['A']['MultiJet'].append("HLT_L1DoubleJet36Central_v4")
        self.referenceMapping['A']['MultiJet'].append("HLT_L1ETM30_v4")
        self.referenceMapping['A']['MultiJet'].append("HLT_L1MultiJet_v4")
        self.referenceMapping['A']['MultiJet'].append("HLT_QuadJet40_IsoPFTau40_v12")
        self.referenceMapping['A']['MultiJet'].append("HLT_QuadJet40_v7")
        self.referenceMapping['A']['MultiJet'].append("HLT_QuadJet45_IsoPFTau45_v7")
        self.referenceMapping['A']['MultiJet'].append("HLT_QuadJet50_DiJet40_v1")
        self.referenceMapping['A']['MultiJet'].append("HLT_QuadJet50_Jet40_Jet30_v3")
        self.referenceMapping['A']['MultiJet'].append("HLT_QuadJet70_v6")
        self.referenceMapping['A']['MultiJet'].append("HLT_QuadJet80_v1")
        self.referenceMapping['A']['Photon'] = []
        self.referenceMapping['A']['Photon'].append("HLT_DoubleEle33_CaloIdL_v5")
        self.referenceMapping['A']['Photon'].append("HLT_DoubleEle45_CaloIdL_v4")
        self.referenceMapping['A']['Photon'].append("HLT_DoublePhoton33_HEVT_v4")
        self.referenceMapping['A']['Photon'].append("HLT_DoublePhoton38_HEVT_v3")
        self.referenceMapping['A']['Photon'].append("HLT_DoublePhoton40_MR150_v6")
        self.referenceMapping['A']['Photon'].append("HLT_DoublePhoton40_R014_MR150_v6")
        self.referenceMapping['A']['Photon'].append("HLT_DoublePhoton5_IsoVL_CEP_v7")
        self.referenceMapping['A']['Photon'].append("HLT_DoublePhoton60_v4")
        self.referenceMapping['A']['Photon'].append("HLT_DoublePhoton80_v2")
        self.referenceMapping['A']['Photon'].append("HLT_Photon135_v2")
        self.referenceMapping['A']['Photon'].append("HLT_Photon200_NoHE_v4")
        self.referenceMapping['A']['Photon'].append("HLT_Photon20_CaloIdVL_IsoL_v7")
        self.referenceMapping['A']['Photon'].append("HLT_Photon20_R9Id_Photon18_R9Id_v7")
        self.referenceMapping['A']['Photon'].append("HLT_Photon225_NoHE_v2")
        self.referenceMapping['A']['Photon'].append("HLT_Photon26_CaloIdXL_IsoXL_Photon18_CaloIdXL_IsoXL_v1")
        self.referenceMapping['A']['Photon'].append("HLT_Photon26_CaloIdXL_IsoXL_Photon18_R9Id_v1")
        self.referenceMapping['A']['Photon'].append("HLT_Photon26_CaloIdXL_IsoXL_Photon18_v1")
        self.referenceMapping['A']['Photon'].append("HLT_Photon26_Photon18_v7")
        self.referenceMapping['A']['Photon'].append("HLT_Photon26_R9Id_Photon18_CaloIdXL_IsoXL_v1")
        self.referenceMapping['A']['Photon'].append("HLT_Photon26_R9Id_Photon18_R9Id_v4")
        self.referenceMapping['A']['Photon'].append("HLT_Photon30_CaloIdVL_IsoL_v9")
        self.referenceMapping['A']['Photon'].append("HLT_Photon30_CaloIdVL_v8")
        self.referenceMapping['A']['Photon'].append("HLT_Photon36_CaloIdL_IsoVL_Photon22_CaloIdL_IsoVL_v4")
        self.referenceMapping['A']['Photon'].append("HLT_Photon36_CaloIdL_IsoVL_Photon22_R9Id_v3")
        self.referenceMapping['A']['Photon'].append("HLT_Photon36_CaloIdL_IsoVL_Photon22_v5")
        self.referenceMapping['A']['Photon'].append("HLT_Photon36_CaloIdVL_Photon22_CaloIdVL_v2")
        self.referenceMapping['A']['Photon'].append("HLT_Photon36_Photon22_v1")
        self.referenceMapping['A']['Photon'].append("HLT_Photon36_R9Id_Photon22_CaloIdL_IsoVL_v4")
        self.referenceMapping['A']['Photon'].append("HLT_Photon36_R9Id_Photon22_R9Id_v3")
        self.referenceMapping['A']['Photon'].append("HLT_Photon400_v2")
        self.referenceMapping['A']['Photon'].append("HLT_Photon44_CaloIdL_Photon34_CaloIdL_v2")
        self.referenceMapping['A']['Photon'].append("HLT_Photon48_CaloIdL_Photon38_CaloIdL_v2")
        self.referenceMapping['A']['Photon'].append("HLT_Photon50_CaloIdVL_IsoL_v7")
        self.referenceMapping['A']['Photon'].append("HLT_Photon50_CaloIdVL_v4")
        self.referenceMapping['A']['Photon'].append("HLT_Photon75_CaloIdVL_IsoL_v8")
        self.referenceMapping['A']['Photon'].append("HLT_Photon75_CaloIdVL_v7")
        self.referenceMapping['A']['Photon'].append("HLT_Photon90_CaloIdVL_IsoL_v5")
        self.referenceMapping['A']['Photon'].append("HLT_Photon90_CaloIdVL_v4")
        self.referenceMapping['A']['PhotonHad'] = []
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon30_CaloIdVT_CentralJet20_BTagIP_v3")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon40_CaloIdL_R005_MR150_v5")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon40_CaloIdL_R017_MR500_v3")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon40_CaloIdL_R023_MR350_v3")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon40_CaloIdL_R029_MR250_v3")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon40_CaloIdL_R042_MR200_v3")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon55_CaloIdL_R017_MR500_v1")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon55_CaloIdL_R023_MR350_v1")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon55_CaloIdL_R029_MR250_v1")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon55_CaloIdL_R042_MR200_v1")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon70_CaloIdL_HT400_v3")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon70_CaloIdL_HT500_v1")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon70_CaloIdL_MHT110_v1")
        self.referenceMapping['A']['PhotonHad'].append("HLT_Photon70_CaloIdL_MHT90_v3")
        self.referenceMapping['A']['SingleElectron'] = []
        self.referenceMapping['A']['SingleElectron'].append("HLT_Ele100_CaloIdVL_CaloIsoVL_TrkIdVL_TrkIsoVL_v3")
        self.referenceMapping['A']['SingleElectron'].append("HLT_Ele25_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_v5")
        self.referenceMapping['A']['SingleElectron'].append("HLT_Ele27_WP80_PFMT50_v4")
        self.referenceMapping['A']['SingleElectron'].append("HLT_Ele32_CaloIdVL_CaloIsoVL_TrkIdVL_TrkIsoVL_v5")
        self.referenceMapping['A']['SingleElectron'].append("HLT_Ele32_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v7")
        self.referenceMapping['A']['SingleElectron'].append("HLT_Ele32_WP70_PFMT50_v4")
        self.referenceMapping['A']['SingleElectron'].append("HLT_Ele65_CaloIdVT_TrkIdT_v4")
        self.referenceMapping['A']['SingleMu'] = []
        self.referenceMapping['A']['SingleMu'].append("HLT_IsoMu15_eta2p1_v1")
        self.referenceMapping['A']['SingleMu'].append("HLT_IsoMu15_v14")
        self.referenceMapping['A']['SingleMu'].append("HLT_IsoMu17_v14")
        self.referenceMapping['A']['SingleMu'].append("HLT_IsoMu20_v9")
        self.referenceMapping['A']['SingleMu'].append("HLT_IsoMu24_eta2p1_v3")
        self.referenceMapping['A']['SingleMu'].append("HLT_IsoMu24_v9")
        self.referenceMapping['A']['SingleMu'].append("HLT_IsoMu30_eta2p1_v3")
        self.referenceMapping['A']['SingleMu'].append("HLT_IsoMu34_eta2p1_v1")
        self.referenceMapping['A']['SingleMu'].append("HLT_L1SingleMu10_v4")
        self.referenceMapping['A']['SingleMu'].append("HLT_L1SingleMu20_v4")
        self.referenceMapping['A']['SingleMu'].append("HLT_L2Mu10_v6")
        self.referenceMapping['A']['SingleMu'].append("HLT_L2Mu20_v6")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu100_eta2p1_v1")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu12_v8")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu15_v9")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu20_v8")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu24_eta2p1_v1")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu24_v8")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu30_eta2p1_v1")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu30_v8")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu40_eta2p1_v1")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu40_v6")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu5_v10")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu60_eta2p1_v1")
        self.referenceMapping['A']['SingleMu'].append("HLT_Mu8_v8")
        self.referenceMapping['A']['Tau'] = []
        self.referenceMapping['A']['Tau'].append("HLT_DoubleIsoPFTau45_Trk5_eta2p1_v3")
        self.referenceMapping['A']['Tau'].append("HLT_IsoPFTau40_IsoPFTau30_Trk5_eta2p1_v3")
        self.referenceMapping['A']['Tau'].append("HLT_MediumIsoPFTau35_Trk20_MET60_v1")
        self.referenceMapping['A']['Tau'].append("HLT_MediumIsoPFTau35_Trk20_MET70_v1")
        self.referenceMapping['A']['Tau'].append("HLT_MediumIsoPFTau35_Trk20_v1")
        self.referenceMapping['A']['TauPlusX'] = []
        self.referenceMapping['A']['TauPlusX'].append("HLT_Ele18_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_MediumIsoPFTau20_v1")
        self.referenceMapping['A']['TauPlusX'].append("HLT_Ele18_CaloIdVT_TrkIdT_MediumIsoPFTau20_v1")
        self.referenceMapping['A']['TauPlusX'].append("HLT_Ele20_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_MediumIsoPFTau20_v1")
        self.referenceMapping['A']['TauPlusX'].append("HLT_HT300_DoubleIsoPFTau10_Trk3_PFMHT40_v8")
        self.referenceMapping['A']['TauPlusX'].append("HLT_HT350_DoubleIsoPFTau10_Trk3_PFMHT45_v8")
        self.referenceMapping['A']['TauPlusX'].append("HLT_IsoMu15_LooseIsoPFTau15_v9")
        self.referenceMapping['A']['TauPlusX'].append("HLT_IsoMu15_eta2p1_LooseIsoPFTau20_v1")
        self.referenceMapping['A']['TauPlusX'].append("HLT_IsoMu15_eta2p1_MediumIsoPFTau20_v1")
        self.referenceMapping['A']['TauPlusX'].append("HLT_IsoMu15_eta2p1_TightIsoPFTau20_v1")
        self.referenceMapping['A']['TauPlusX'].append("HLT_Mu15_LooseIsoPFTau15_v9")
        self.referenceMapping['A']['TauPlusX'].append("HLT_QuadJet50_IsoPFTau50_v1")
        self.referenceMapping['ALCAP0'] = {}
        self.referenceMapping['ALCAP0']['AlCaP0'] = []
        self.referenceMapping['ALCAP0']['AlCaP0'].append("AlCa_EcalEta_v9")
        self.referenceMapping['ALCAP0']['AlCaP0'].append("AlCa_EcalPi0_v10")
        self.referenceMapping['ALCAPHISYM'] = {}
        self.referenceMapping['ALCAPHISYM']['AlCaPhiSym'] = []
        self.referenceMapping['ALCAPHISYM']['AlCaPhiSym'].append("AlCa_EcalPhiSym_v7")
        self.referenceMapping['Calibration'] = {}
        self.referenceMapping['Calibration']['TestEnablesEcalHcalDT'] = []
        self.referenceMapping['Calibration']['TestEnablesEcalHcalDT'].append("HLT_DTCalibration_v1")
        self.referenceMapping['Calibration']['TestEnablesEcalHcalDT'].append("HLT_EcalCalibration_v2")
        self.referenceMapping['Calibration']['TestEnablesEcalHcalDT'].append("HLT_HcalCalibration_v2")
        self.referenceMapping['EcalCalibration'] = {}
        self.referenceMapping['EcalCalibration']['EcalLaser'] = []
        self.referenceMapping['EcalCalibration']['EcalLaser'].append("HLT_EcalCalibration_v2")
        self.referenceMapping['Express'] = {}
        self.referenceMapping['Express']['ExpressPhysics'] = []
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_DoubleEle45_CaloIdL_v4")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_DoubleMu45_v6")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_DoublePhoton80_v2")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_EightJet120_v1")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_Ele100_CaloIdVL_CaloIsoVL_TrkIdVL_TrkIsoVL_v3")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v8")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_Ele65_CaloIdVT_TrkIdT_v4")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_HT2000_v2")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_Jet370_v6")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_Jet800_v1")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_MET200_v7")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_MET400_v2")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_Mu100_eta2p1_v1")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_v4")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_Mu17_Mu8_v7")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_Photon36_CaloIdL_IsoVL_Photon22_CaloIdL_IsoVL_v4")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_Photon400_v2")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_Photon75_CaloIdVL_IsoL_v8")
        self.referenceMapping['Express']['ExpressPhysics'].append("HLT_ZeroBias_v4")
        self.referenceMapping['HLTMON'] = {}
        self.referenceMapping['HLTMON']['OfflineMonitor'] = []
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("AlCa_EcalEta_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("AlCa_EcalPhiSym_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("AlCa_EcalPi0_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("AlCa_RPCMuonNoHits_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("AlCa_RPCMuonNoTriggers_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("AlCa_RPCMuonNormalisation_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_60Jet10_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_70Jet10_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_70Jet13_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Activity_Ecal_SC7_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_BTagMu_DiJet110_Mu5_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_BTagMu_DiJet20_Mu5_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_BTagMu_DiJet40_Mu5_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_BTagMu_DiJet70_Mu5_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_BeamGas_BSC_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_BeamGas_HF_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_BeamHalo_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_CentralJet46_CentralJet38_CentralJet20_DiBTagIP3D_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_CentralJet46_CentralJet38_DiBTagIP3D_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_CentralJet60_CentralJet53_DiBTagIP3D_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_CentralJet80_MET100_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_CentralJet80_MET160_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_CentralJet80_MET65_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_CentralJet80_MET80_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DTErrors_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiCentralJet20_BTagIP_MET65_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiCentralJet20_MET100_HBHENoiseFiltered_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiCentralJet20_MET80_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiCentralJet36_BTagIP3DLoose_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiJet130_PT130_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiJet160_PT160_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiJet60_MET45_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiJetAve110_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiJetAve190_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiJetAve240_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiJetAve300_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiJetAve30_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiJetAve370_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DiJetAve60_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon0_Jpsi_Muon_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon0_Jpsi_NoVertexing_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon0_Jpsi_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon0_Upsilon_Muon_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon0_Upsilon_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon10_Jpsi_Barrel_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon11_PsiPrime_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon13_Jpsi_Barrel_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon6_LowMass_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon7_Upsilon_Barrel_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon9_PsiPrime_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Dimuon9_Upsilon_Barrel_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleEle10_CaloIdL_TrkIdVL_Ele10_CaloIdT_TrkIdVL_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleEle33_CaloIdL_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleEle45_CaloIdL_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleEle8_CaloIdT_TrkIdVL_HT150_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleEle8_CaloIdT_TrkIdVL_Mass4_HT150_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleEle8_CaloIdT_TrkIdVL_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleIsoPFTau45_Trk5_eta2p1_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleJet30_ForwardBackward_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleJet60_ForwardBackward_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleJet70_ForwardBackward_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleJet80_ForwardBackward_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu3_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu45_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu4_Dimuon4_Bs_Barrel_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu4_Dimuon6_Bs_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu4_Jpsi_Displaced_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu4p5_LowMass_Displaced_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu5_Acoplanarity03_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu5_Ele8_CaloIdL_TrkIdVL_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu5_Ele8_CaloIdT_TrkIdVL_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu5_HT150_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu5_IsoMu5_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu5_Jpsi_Displaced_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu5_LowMass_Displaced_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu5_Mass4_HT150_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu5_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu6_Acoplanarity03_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu6_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoubleMu7_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoublePhoton33_HEVT_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoublePhoton38_HEVT_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoublePhoton40_MR150_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoublePhoton40_R014_MR150_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoublePhoton5_IsoVL_CEP_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoublePhoton60_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_DoublePhoton80_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_EightJet120_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele100_CaloIdVL_CaloIsoVL_TrkIdVL_TrkIsoVL_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele12_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_R005_MR200_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele12_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_R025_MR200_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele12_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_R029_MR200_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele15_CaloIdT_CaloIsoVL_TrkIdT_TrkIsoVL_HT250_PFMHT25_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele15_CaloIdT_CaloIsoVL_TrkIdT_TrkIsoVL_HT250_PFMHT40_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele15_CaloIdT_CaloIsoVL_TrkIdT_TrkIsoVL_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele17_CaloIdL_CaloIsoVL_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele17_CaloIdVT_CaloIsoVT_TrkIdT_TrkIsoVT_Ele8_Mass30_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele17_CaloIdVT_CaloIsoVT_TrkIdT_TrkIsoVT_SC8_Mass30_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele18_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_MediumIsoPFTau20_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele18_CaloIdVT_TrkIdT_MediumIsoPFTau20_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele20_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_Jet35_Jet25_Deta3_Jet20_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele20_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_MediumIsoPFTau20_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele22_CaloIdL_CaloIsoVL_Ele15_HFT_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele25_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralJet30_BTagIP_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralJet30_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_DiCentralJet30_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_QuadCentralJet30_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralJet30_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele25_CaloIdVT_TrkIdT_CentralJet30_BTagIP_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele25_CaloIdVT_TrkIdT_CentralJet30_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele25_CaloIdVT_TrkIdT_DiCentralJet30_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele25_CaloIdVT_TrkIdT_QuadCentralJet30_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele25_CaloIdVT_TrkIdT_TriCentralJet30_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralJet30_CentralJet25_PFMHT20_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralJet30_CentralJet25_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_Jet35_Jet25_Deta3_Jet20_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele27_CaloIdVT_TrkIdT_CentralJet30_CentralJet25_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele27_CaloIdVT_TrkIdT_Jet35_Jet25_Deta3_Jet20_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele27_WP80_PFMT50_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele30_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_DiCentralJet30_PFMHT25_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele30_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_Jet35_Jet25_Deta3p5_Jet25_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele32_CaloIdT_CaloIsoT_TrkIdT_TrkIsoT_Ele17_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele32_CaloIdT_CaloIsoT_TrkIdT_TrkIsoT_SC17_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele32_CaloIdVL_CaloIsoVL_TrkIdVL_TrkIsoVL_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele32_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele32_WP70_PFMT50_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele65_CaloIdVT_TrkIdT_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele8_CaloIdL_CaloIsoVL_Jet40_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele8_CaloIdL_CaloIsoVL_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele8_CaloIdL_TrkIdVL_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele8_CaloIdT_TrkIdT_DiJet30_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele8_CaloIdT_TrkIdT_QuadJet30_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele8_CaloIdT_TrkIdT_TriJet30_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Ele8_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_ExclDiJet60_HFAND_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_ExclDiJet60_HFOR_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_FatJetMass750_DR1p1_Deta2p0_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_FatJetMass850_DR1p1_Deta2p0_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_GlobalRunHPDNoise_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT150_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT2000_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT200_AlphaT0p55_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT200_DoubleEle5_CaloIdVL_MassJPsi_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT200_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT250_AlphaT0p53_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT250_AlphaT0p55_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT250_DoubleDisplacedJet60_PromptTrack_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT250_DoubleDisplacedJet60_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT250_MHT100_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT250_MHT90_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT250_Mu15_PFMHT40_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT250_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_AlphaT0p53_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_AlphaT0p54_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_CentralJet30_BTagIP_PFMHT55_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_CentralJet30_BTagIP_PFMHT65_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_CentralJet30_BTagIP_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_DoubleIsoPFTau10_Trk3_PFMHT40_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_Ele5_CaloIdVL_CaloIsoVL_TrkIdVL_TrkIsoVL_PFMHT40_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_MHT80_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_MHT90_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_Mu15_PFMHT40_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_Mu5_PFMHT40_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_PFMHT55_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_PFMHT65_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT300_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT350_AlphaT0p52_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT350_AlphaT0p53_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT350_DoubleIsoPFTau10_Trk3_PFMHT45_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT350_Ele30_CaloIdT_TrkIdT_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT350_Ele5_CaloIdVL_CaloIsoVL_TrkIdVL_TrkIsoVL_PFMHT45_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT350_MHT70_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT350_MHT80_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT350_MHT90_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT350_Mu5_PFMHT45_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT350_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT400_AlphaT0p51_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT400_AlphaT0p52_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT400_Ele60_CaloIdT_TrkIdT_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT400_MHT80_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT400_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT450_AlphaT0p51_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT450_AlphaT0p52_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT450_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT500_JetPt60_DPhi2p94_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT500_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT550_JetPt60_DPhi2p94_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT550_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT600_JetPt60_DPhi2p94_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT600_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HT650_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HcalNZS_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_HcalPhiSym_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu15_LooseIsoPFTau15_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu15_eta2p1_LooseIsoPFTau20_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu15_eta2p1_MediumIsoPFTau20_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu15_eta2p1_TightIsoPFTau20_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu15_eta2p1_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu15_v14")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu17_eta2p1_CentralJet30_BTagIP_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu17_eta2p1_CentralJet30_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu17_eta2p1_DiCentralJet30_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu17_eta2p1_QuadCentralJet30_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu17_eta2p1_TriCentralJet30_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu17_v14")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu20_DiCentralJet34_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu20_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu24_eta2p1_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu24_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu30_eta2p1_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoMu34_eta2p1_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoPFTau40_IsoPFTau30_Trk5_eta2p1_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoTrackHB_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_IsoTrackHE_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Jet110_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Jet190_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Jet240_CentralJet30_BTagIP_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Jet240_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Jet270_CentralJet30_BTagIP_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Jet300_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Jet30_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Jet370_NoJetID_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Jet370_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Jet60_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Jet800_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_JetE30_NoBPTX3BX_NoHalo_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_JetE30_NoBPTX_NoHalo_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_JetE30_NoBPTX_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_JetE50_NoBPTX3BX_NoHalo_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1DoubleJet36Central_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1DoubleMu0_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1ETM30_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1MultiJet_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1SingleEG12_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1SingleEG5_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1SingleJet16_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1SingleJet36_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1SingleMu10_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1SingleMu20_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1SingleMuOpen_AntiBPTX_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1SingleMuOpen_DT_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1SingleMuOpen_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1Tech_HBHEHO_totalOR_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1Tech_HCAL_HF_single_channel_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1TrackerCosmics_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1_Interbunch_BSC_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L1_PreCollisions_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L2DoubleMu0_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L2DoubleMu23_NoVertex_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L2DoubleMu30_NoVertex_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L2Mu10_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L2Mu20_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L2Mu60_1Hit_MET40_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_L2Mu60_1Hit_MET60_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_LogMonitor_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MET100_HBHENoiseFiltered_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MET100_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MET120_HBHENoiseFiltered_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MET120_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MET200_HBHENoiseFiltered_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MET200_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MET400_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MET65_HBHENoiseFiltered_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MET65_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MediumIsoPFTau35_Trk20_MET60_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MediumIsoPFTau35_Trk20_MET70_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_MediumIsoPFTau35_Trk20_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu100_eta2p1_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu10_R005_MR200_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu10_R025_MR200_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu10_R029_MR200_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu12_eta2p1_DiCentralJet20_BTagIP3D1stTrack_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu12_eta2p1_DiCentralJet20_DiBTagIP3D1stTrack_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu12_eta2p1_DiCentralJet30_BTagIP3D_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu12_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu13_Mu8_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu15_DoublePhoton15_CaloIdL_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu15_LooseIsoPFTau15_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu15_Photon20_CaloIdL_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu15_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu17_Ele8_CaloIdL_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu17_Mu8_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu17_eta2p1_CentralJet30_BTagIP_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu17_eta2p1_CentralJet30_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu17_eta2p1_DiCentralJet30_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu17_eta2p1_QuadCentralJet30_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu17_eta2p1_TriCentralJet30_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu20_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu24_eta2p1_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu24_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu30_eta2p1_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu30_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu40_HT200_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu40_eta2p1_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu40_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_DiJet30_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_DoubleEle8_CaloIdT_TrkIdVL_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_Ele8_CaloIdT_CaloIsoVL_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_Ele8_CaloIdT_TrkIdVL_Ele8_CaloIdL_TrkIdVL_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_Ele8_CaloIdT_TrkIdVL_HT150_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_Ele8_CaloIdT_TrkIdVL_Mass4_HT150_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_L2Mu2_Jpsi_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_QuadJet30_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_TkMu0_OST_Jpsi_Tight_B5Q7_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_Track2_Jpsi_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_TriJet30_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu5_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu60_HT200_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu60_eta2p1_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu7_Track7_Jpsi_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu8_Ele17_CaloIdL_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu8_Jet40_v10")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu8_Photon20_CaloIdVT_IsoT_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Mu8_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_PFMHT150_v12")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon135_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon200_NoHE_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon20_CaloIdVL_IsoL_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon20_CaloIdVT_IsoT_Ele8_CaloIdL_CaloIsoVL_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon20_R9Id_Photon18_R9Id_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon225_NoHE_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon26_CaloIdXL_IsoXL_Photon18_CaloIdXL_IsoXL_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon26_CaloIdXL_IsoXL_Photon18_R9Id_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon26_CaloIdXL_IsoXL_Photon18_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon26_Photon18_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon26_R9Id_Photon18_CaloIdXL_IsoXL_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon26_R9Id_Photon18_R9Id_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon30_CaloIdVL_IsoL_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon30_CaloIdVL_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon30_CaloIdVT_CentralJet20_BTagIP_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon36_CaloIdL_IsoVL_Photon22_CaloIdL_IsoVL_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon36_CaloIdL_IsoVL_Photon22_R9Id_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon36_CaloIdL_IsoVL_Photon22_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon36_CaloIdVL_Photon22_CaloIdVL_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon36_Photon22_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon36_R9Id_Photon22_CaloIdL_IsoVL_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon36_R9Id_Photon22_R9Id_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon400_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon40_CaloIdL_R005_MR150_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon40_CaloIdL_R017_MR500_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon40_CaloIdL_R023_MR350_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon40_CaloIdL_R029_MR250_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon40_CaloIdL_R042_MR200_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon44_CaloIdL_Photon34_CaloIdL_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon48_CaloIdL_Photon38_CaloIdL_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon50_CaloIdVL_IsoL_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon50_CaloIdVL_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon55_CaloIdL_R017_MR500_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon55_CaloIdL_R023_MR350_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon55_CaloIdL_R029_MR250_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon55_CaloIdL_R042_MR200_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon70_CaloIdL_HT400_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon70_CaloIdL_HT500_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon70_CaloIdL_MHT110_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon70_CaloIdL_MHT90_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon75_CaloIdVL_IsoL_v8")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon75_CaloIdVL_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon90_CaloIdVL_IsoL_v5")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Photon90_CaloIdVL_v4")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Physics_v2")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_PixelTracks_Multiplicity100_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_PixelTracks_Multiplicity80_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_QuadJet40_IsoPFTau40_v12")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_QuadJet40_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_QuadJet45_IsoPFTau45_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_QuadJet50_DiJet40_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_QuadJet50_IsoPFTau50_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_QuadJet50_Jet40_Jet30_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_QuadJet70_v6")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_QuadJet80_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_R014_MR150_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_R020_MR150_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_R020_MR550_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_R023_MR550_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_R025_MR150_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_R025_MR450_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_R029_MR450_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_R033_MR350_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_R036_MR350_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_R038_MR250_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_R042_MR250_v3")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_Random_v1")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_RegionalCosmicTracking_v7")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_TripleEle10_CaloIdL_TrkIdVL_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_TripleMu5_v9")
        self.referenceMapping['HLTMON']['OfflineMonitor'].append("HLT_ZeroBias_v4")
        self.referenceMapping['NanoDST'] = {}
        self.referenceMapping['NanoDST']['L1Accept'] = []
        self.referenceMapping['NanoDST']['L1Accept'].append("DST_Physics_v2")
        self.referenceMapping['RPCMON'] = {}
        self.referenceMapping['RPCMON']['RPCMonitor'] = []
        self.referenceMapping['RPCMON']['RPCMonitor'].append("AlCa_RPCMuonNoHits_v6")
        self.referenceMapping['RPCMON']['RPCMonitor'].append("AlCa_RPCMuonNoTriggers_v6")
        self.referenceMapping['RPCMON']['RPCMonitor'].append("AlCa_RPCMuonNormalisation_v6")
        self.referenceMapping['TrackerCalibration'] = {}
        self.referenceMapping['TrackerCalibration']['TestEnablesTracker'] = []
        self.referenceMapping['TrackerCalibration']['TestEnablesTracker'].append("HLT_TrackerCalibration_v2")

        # remember for later
        self.insertRunDAO = daoFactory(classname = "RunConfig.InsertRun")
        self.insertLumiDAO = daoFactory(classname = "RunConfig.InsertLumiSection")
        self.insertStreamCMSSWVersionDAO = daoFactory(classname = "RunConfig.InsertStreamCMSSWVersion")
        self.insertStreamerDAO = daoFactory(classname = "RunConfig.InsertStreamer")
        self.findNewRunsDAO = daoFactory(classname = "Tier0Feeder.FindNewRuns")
        self.findNewRunStreamsDAO = daoFactory(classname = "Tier0Feeder.FindNewRunStreams")
        self.feedStreamersDAO = daoFactory(classname = "Tier0Feeder.FeedStreamers")
        self.insertClosedLumiDAO = daoFactory(classname = "RunLumiCloseout.InsertClosedLumi")
        self.finalCloseLumiDAO = daoFactory(classname = "RunLumiCloseout.FinalCloseLumi")
        self.insertSplitLumisDAO = daoFactory(classname = "JobSplitting.InsertSplitLumis")
        self.findNewExpressRunsDAO = daoFactory(classname = "Tier0Feeder.FindNewExpressRuns")
        self.releaseExpressDAO = daoFactory(classname = "Tier0Feeder.ReleaseExpress")

        self.getStreamerWorkflowsForMonitoringDAO = daoFactory(classname = "Tier0Feeder.GetStreamerWorkflowsForMonitoring")
        self.getPromptRecoWorkflowsForMonitoringDAO = daoFactory(classname = "Tier0Feeder.GetPromptRecoWorkflowsForMonitoring")
        self.markTrackedWorkflowMonitoringDAO = daoFactory(classname = "Tier0Feeder.MarkTrackedWorkflowMonitoring")

        return

    def tearDown(self):
        """
        _tearDown_

        """
        self.testInit.clearDatabase()

        return


    def changeActiveLumiSplits(self, lumi ):
        """
        __

        It deletes a lumi subscription from one table and inserts it onto the completed table
        """

        myThread = threading.currentThread()

        myThread.dbi.processData("""INSERT INTO wmbs_sub_files_complete (fileid, subscription)
                                    SELECT
                                        fileid,
                                        subscription
                                    FROM
                                        wmbs_sub_files_available
                                    WHERE 
                                        fileid = '%s'
                                           """ % lumi, transaction = False)

        myThread.dbi.processData("""DELETE FROM wmbs_sub_files_available
                                    WHERE fileid = '%s'
                                             """ % lumi, transaction = False)
        return

 
    def insertLocation(self, pnn):
        """
        __

        it is inserting a pnn location
        """
        myThread = threading.currentThread()

        myThread.dbi.processData("""INSERT INTO wmbs_pnns (id, pnn)
                                    VALUES (wmbs_pnns_SEQ.nextval, '%s')
                                    """ % pnn, transaction = False)

        return

    def insertRun(self, run):
        """
        _insertRun_

        insert run and lumi records for given run

        """
        self.insertRunDAO.execute(binds = { 'RUN' : run,
                                            'HLTKEY' : self.hltkey },
                                  transaction = False)

        return

    def insertRunStreamLumi(self, run, stream, lumi):
        """
        _insertRunStreamLumi_

        insert run/stream/cmssw assoc and single streamer with given lumi

        """
        self.insertStreamCMSSWVersionDAO.execute(binds = { 'RUN' : run,
                                                           'STREAM' : stream,
                                                           'VERSION' : "CMSSW_4_2_7" },
                                                 transaction = False)

        self.insertLumiDAO.execute(binds = { 'RUN' : run,
                                             'LUMI' : lumi },
                                   transaction = False)

        self.insertStreamerDAO.execute(streamerPNN =self.tier0Config.Global.StreamerPNN,
                                       binds = { 'RUN' : run,
                                                 'P5_ID': self.p5id, 
                                                 'LUMI' : lumi,
                                                 'STREAM' : stream, 
                                                 'LFN' : makeUUID(),
                                                 'FILESIZE' : 100,
                                                 'EVENTS' : 100,
                                                 'TIME' : int(time.time()) },
                                       transaction = False)

        return

    def feedStreamers(self):
        """
        _feedStreamers_

        helper function to wrap the feedStreamersDAO
        call into an transaction

        """
        myThread = threading.currentThread()

        myThread.transaction.begin()
        self.feedStreamersDAO.execute(conn = myThread.transaction.conn, transaction = True)
        myThread.transaction.commit()

        return

    def getNumFeedStreamers(self):
        """
        _getNumFeedStreamers_

        helper function that counts the number of feed streamers

        """
        myThread = threading.currentThread()

        results = myThread.dbi.processData("""SELECT COUNT(*)
                                              FROM wmbs_sub_files_available
                                              """, transaction = False)[0].fetchall()
        return results[0][0]

    def getNumActiveSplitLumis(self):
        """
        _getNumActiveSplitLumis_

        helper function that counts the number of active split lumis
        """
        myThread = threading.currentThread()

        results = myThread.dbi.processData("""SELECT COUNT(*)
                                              FROM lumi_section_split_active
                                              """, transaction = False)[0].fetchall()

        return results[0][0]

    def getClosedLumis(self):
        """
        _getClosedLumis_

        helper function that retrieves the closed lumis

        """
        myThread = threading.currentThread()

        results = myThread.dbi.processData("""SELECT lumi_section_closed.run_id,
                                                     stream.name,
                                                     lumi_section_closed.lumi_id,
                                                     lumi_section_closed.filecount
                                              FROM lumi_section_closed
                                              INNER JOIN stream ON
                                                stream.id = lumi_section_closed.stream_id
                                              """, transaction = False)[0].fetchall()

        runStreamLumiDict = {}
        for result in results:

            run = result[0]
            stream = result[1]
            lumi = result[2]
            filecount = result[3]

            if run not in runStreamLumiDict:
                runStreamLumiDict[run] = {}
            if stream not in runStreamLumiDict[run]:
                runStreamLumiDict[run][stream] = {}

            runStreamLumiDict[run][stream][lumi] = filecount

        return runStreamLumiDict

    def getEndedRuns(self):
        """
        _getEndedRuns_

        helper function that retrieves the ended runs

        """
        myThread = threading.currentThread()
 
        results = myThread.dbi.processData("""SELECT run_id, lumicount
                                                      FROM run
                                                      WHERE close_time > 0
                                                      """, transaction = False)[0].fetchall()

        runLumiDict = {}
        for result in results:
            runLumiDict[result[0]] = result[1]

        return runLumiDict

    def getClosedRunStreamFilesets(self):
        """
        _getClosedRunStreamFilesets_

        helper function that retrieves closed run/stream filesets

        """
        myThread = threading.currentThread()

        results = myThread.dbi.processData("""SELECT run_stream_fileset_assoc.run_id,
                                                     stream.name
                                              FROM run_stream_fileset_assoc
                                              INNER JOIN wmbs_fileset ON
                                                wmbs_fileset.id = run_stream_fileset_assoc.fileset AND
                                                wmbs_fileset.open = 0
                                              INNER JOIN stream ON
                                                stream.id = run_stream_fileset_assoc.stream_id
                                              """, transaction = False)[0].fetchall()

        runStreamDict = {}
        for result in results:
            runStreamDict[result[0]] = result[1]

        return runStreamDict

    def feedCouchMonitoring(self):
        """
        _feedCouchMonitoring_

        check for workflows that haven't been uploaded to Couch for monitoring yet

        """
        workflows = self.getStreamerWorkflowsForMonitoringDAO.execute()
        workflows += self.getPromptRecoWorkflowsForMonitoringDAO.execute()

        if len(workflows) == 0:
            logging.debug("No workflows to publish to couch monitoring, doing nothing")

        if workflows:
            logging.debug(" Going to publish %d workflows" % len(workflows))
            for (workflowId, run, workflowName) in workflows:
                logging.info(" Publishing workflow %s to monitoring" % workflowName)
                doc = {}
                doc["RequestName"] = workflowName
                doc["Run"] = run
                response = self.localRequestCouchDB.insertGenericRequest(doc)
                if response == "OK" or "EXISTS":
                    logging.info(" Successfully uploaded request %s" % workflowName)
                    self.markTrackedWorkflowMonitoringDAO.execute(workflowId)

        return

    def test00(self):
        """
        _test00_

        Test the FindNewRuns, FindNewRunStreams and FeedStreamers DAOs
        and their interaction with the RunConfigAPI.configureRun and
        RunConfigAPI.configureRunStream methods

        Don't test the interaction with the StorageManager DB to close
        lumis, we instead close lumis directly and just test that
        the system behaves correctly with open/closed lumis.

        """
        runs = self.findNewRunsDAO.execute(transaction = False)
        self.assertEqual(len(runs), 0,
                         "ERROR: there should be no new run")

        runStreams = self.findNewRunStreamsDAO.execute(transaction = False)
        self.assertEqual(len(list(runStreams.keys())), 0,
                         "ERROR: there should be no new run/stream")

        self.feedStreamers()
        self.assertEqual(self.getNumFeedStreamers(), 0,
                         "ERROR: there should be no streamers feed")

        self.insertRun(176161)
        self.insertRunStreamLumi(176161, "A", 1)

        runs = self.findNewRunsDAO.execute(transaction = False)
        self.assertEqual(len(runs), 1,
                         "ERROR: there should be one new run")
        runStreams = self.findNewRunStreamsDAO.execute(transaction = False)
        self.assertEqual(len(list(runStreams.keys())), 0,
                         "ERROR: there should be no new run/stream")

        RunConfigAPI.configureRun(self.tier0Config, 176161,
                                  self.hltConfig,
                                  { 'process' : "HLT",
                                    'mapping' : self.referenceMapping })

        runs = self.findNewRunsDAO.execute(transaction = False)
        self.assertEqual(len(runs), 0,
                         "ERROR: there should be no new run")

        self.feedStreamers()
        self.assertEqual(self.getNumFeedStreamers(), 0,
                         "ERROR: there should be no streamers feed")

        runStreams = self.findNewRunStreamsDAO.execute(transaction = False)
        self.assertEqual(set(runStreams.keys()), set([176161]),
                         "ERROR: there should be new run/stream for run 176161")
        self.assertEqual(set(runStreams[176161]), set(["A"]),
                         "ERROR: there should be new run/stream for run 176161 and stream A")

        RunConfigAPI.configureRunStream(self.tier0Config, 176161, "A", self.testDir, self.dqmUploadProxy)

        runStreams = self.findNewRunStreamsDAO.execute(transaction = False)
        self.assertEqual(len(list(runStreams.keys())), 0,
                         "ERROR: there should be no new run/stream")

        self.feedStreamers()
        self.assertEqual(self.getNumFeedStreamers(), 0,
                         "ERROR: there should be no streamers feed")

        self.insertClosedLumiDAO.execute(binds = { 'RUN' : 176161,
                                                   'LUMI' : 1,
                                                   'STREAM' : 'A',
                                                   'FILECOUNT' : 1,
                                                   'INSERT_TIME' : int(time.time()),
                                                   'CLOSE_TIME' : 0 },
                                         conn = None,
                                         transaction = False)

        self.feedStreamers()
        self.assertEqual(self.getNumFeedStreamers(), 0,
                         "ERROR: there should be no streamers feed")
        self.finalCloseLumiDAO.execute(int(time.time()), conn=None, transaction = False)
                                       
        self.feedStreamers()
        self.assertEqual(self.getNumFeedStreamers(), 1,
                         "ERROR: there should be 1 streamers feed")

        self.insertRunStreamLumi(176161, "A", 2)

        self.feedStreamers()
        self.assertEqual(self.getNumFeedStreamers(), 1,
                         "ERROR: there should be 1 streamers feed")

        self.insertClosedLumiDAO.execute(binds = { 'RUN' : 176161,
                                                   'STREAM' : 'A',
                                                   'LUMI' : 2,
                                                   'INSERT_TIME' : int(time.time()),
                                                   'CLOSE_TIME' : int(time.time()),
                                                   'FILECOUNT' : 1 },
                                         transaction = False)

        self.feedStreamers()
        self.assertEqual(self.getNumFeedStreamers(), 2,
                         "ERROR: there should be 2 streamers feed")

        self.insertRunStreamLumi(176161, "A", 3)

        self.feedStreamers()
        self.assertEqual(self.getNumFeedStreamers(), 2,
                         "ERROR: there should be 2 streamers feed")

        self.insertClosedLumiDAO.execute(binds = { 'RUN' : 176161,
                                                   'STREAM' : 'A',
                                                   'LUMI' : 3,
                                                   'INSERT_TIME' : int(time.time()),
                                                   'CLOSE_TIME' : 0,
                                                   'FILECOUNT' : 2 },
                                         transaction = False)

        self.feedStreamers()
        self.assertEqual(self.getNumFeedStreamers(), 2,
                         "ERROR: there should be 2 streamers feed")

        self.finalCloseLumiDAO.execute(int(time.time()), transaction = False)
                                       
        self.feedStreamers()
        self.assertEqual(self.getNumFeedStreamers(), 2,
                         "ERROR: there should be 2 streamers feed")

        self.insertRunStreamLumi(176161, "A", 3)

        self.finalCloseLumiDAO.execute(int(time.time()), transaction = False)

        self.feedStreamers()
        self.assertEqual(self.getNumFeedStreamers(), 4,
                         "ERROR: there should be 4 streamers feed")

        self.insertRun(176162)
        self.insertRunStreamLumi(176162, "A", 1)
        self.insertRunStreamLumi(176162, "Express", 1)
        self.insertRunStreamLumi(176162, "HLTMON", 1)

        self.insertRun(176163)
        self.insertRunStreamLumi(176163, "A", 1)
        self.insertRunStreamLumi(176163, "Express", 1)

        runs = self.findNewRunsDAO.execute(transaction = False)
        self.assertEqual(len(runs), 2,
                         "ERROR: there should be two new runs")

        runStreams = self.findNewRunStreamsDAO.execute(transaction = False)
        self.assertEqual(len(list(runStreams.keys())), 0,
                         "ERROR: there should be no new run/stream")

        self.feedStreamers()
        self.assertEqual(self.getNumFeedStreamers(), 4,
                         "ERROR: there should be 4 streamers feed")

        RunConfigAPI.configureRun(self.tier0Config, 176162,
                                  self.hltConfig,
                                  { 'process' : "HLT",
                                    'mapping' : self.referenceMapping })

        runStreams = self.findNewRunStreamsDAO.execute(transaction = False)
        self.assertEqual(set(runStreams.keys()), set([176162]),
                         "ERROR: there should be new run/stream for run 176162")
        self.assertEqual(set(runStreams[176162]), set(["A", "Express", "HLTMON"]),
                         "ERROR: there should be new run/stream for run 176162 and stream A,Express,HLTMON")

        runs = self.findNewRunsDAO.execute(transaction = False)
        self.assertEqual(len(runs), 1,
                         "ERROR: there should be one new run")

        self.feedStreamers()
        self.assertEqual(self.getNumFeedStreamers(), 4,
                         "ERROR: there should be 4 streamers feed")

        RunConfigAPI.configureRun(self.tier0Config, 176163,
                                  self.hltConfig,
                                  { 'process' : "HLT",
                                    'mapping' : self.referenceMapping })

        runs = self.findNewRunsDAO.execute(transaction = False)
        self.assertEqual(len(runs), 0,
                         "ERROR: there should be no new run")

        runStreams = self.findNewRunStreamsDAO.execute(transaction = False)
        self.assertEqual(set(runStreams.keys()), set([176162, 176163]),
                         "ERROR: there should be new run/stream for run 176162 and 176163")
        self.assertEqual(set(runStreams[176162]), set(["A", "Express", "HLTMON"]),
                         "ERROR: there should be new run/stream for run 176162 and stream A, Express and HLTMON")
        self.assertEqual(set(runStreams[176163]), set(["A", "Express"]),
                         "ERROR: there should be new run/stream for run 176162 and stream A and Express")

        self.feedStreamers()
        self.assertEqual(self.getNumFeedStreamers(), 4,
                         "ERROR: there should be 4 streamers feed")

        RunConfigAPI.configureRunStream(self.tier0Config, 176162, "A", self.testDir, self.dqmUploadProxy)
        RunConfigAPI.configureRunStream(self.tier0Config, 176163, "Express", self.testDir, self.dqmUploadProxy)

        runStreams = self.findNewRunStreamsDAO.execute(transaction = False)
        self.assertEqual(set(runStreams.keys()), set([176162, 176163]),
                         "ERROR: there should be new run/stream for run 176162 and 176163")
        self.assertEqual(set(runStreams[176162]), set(["Express", "HLTMON"]),
                         "ERROR: there should be new run/stream for run 176162 and stream Express and HLTMON")
        self.assertEqual(set(runStreams[176163]), set(["A"]),
                         "ERROR: there should be new run/stream for run 176162 and stream A")

        self.feedStreamers()
        self.assertEqual(self.getNumFeedStreamers(), 4,
                         "ERROR: there should be 4 streamers feed")

        self.insertClosedLumiDAO.execute(binds = { 'RUN' : 176162,
                                                   'STREAM' : 'A',
                                                   'LUMI' : 1,
                                                   'INSERT_TIME' : int(time.time()),
                                                   'CLOSE_TIME' : int(time.time()),
                                                   'FILECOUNT' : 1 },
                                         transaction = False)

        self.feedStreamers()
        self.assertEqual(self.getNumFeedStreamers(), 5,
                         "ERROR: there should be 5 streamers feed")


        self.insertClosedLumiDAO.execute(binds = { 'RUN' : 176163,
                                                   'STREAM' : 'Express',
                                                   'LUMI' : 1,
                                                   'INSERT_TIME' : int(time.time()),
                                                   'CLOSE_TIME' : int(time.time()),
                                                   'FILECOUNT' : 1 },
                                         transaction = False)

        self.feedStreamers()
        self.assertEqual(self.getNumFeedStreamers(), 6,
                         "ERROR: there should be 6 streamers feed")

        RunConfigAPI.configureRunStream(self.tier0Config, 176162, "Express", self.testDir, self.dqmUploadProxy)
        RunConfigAPI.configureRunStream(self.tier0Config, 176162, "HLTMON", self.testDir, self.dqmUploadProxy)

        runStreams = self.findNewRunStreamsDAO.execute(transaction = False)
        self.assertEqual(set(runStreams.keys()), set([176163]),
                         "ERROR: there should be new run/stream for run 176163")
        self.assertEqual(set(runStreams[176163]), set(["A"]),
                         "ERROR: there should be new run/stream for run 176163 and stream A")

        self.feedStreamers()
        self.assertEqual(self.getNumFeedStreamers(), 6,
                         "ERROR: there should be 6 streamers feed")

        self.insertClosedLumiDAO.execute(binds = { 'RUN' : 176162,
                                                   'STREAM' : 'Express',
                                                   'LUMI' : 1,
                                                   'INSERT_TIME' : int(time.time()),
                                                   'CLOSE_TIME' : int(time.time()),
                                                   'FILECOUNT' : 1 },
                                         transaction = False)

        self.feedStreamers()
        self.assertEqual(self.getNumFeedStreamers(), 7,
                         "ERROR: there should be 7 streamers feed")

        self.insertClosedLumiDAO.execute(binds = { 'RUN' : 176162,
                                                   'STREAM' : 'HLTMON',
                                                   'LUMI' : 1,
                                                   'INSERT_TIME' : int(time.time()),
                                                   'CLOSE_TIME' : int(time.time()),
                                                   'FILECOUNT' : 1 },
                                         transaction = False)

        self.feedStreamers()
        self.assertEqual(self.getNumFeedStreamers(), 8,
                         "ERROR: there should be 8 streamers feed")

        RunConfigAPI.configureRunStream(self.tier0Config, 176163, "A", self.testDir, self.dqmUploadProxy)

        runStreams = self.findNewRunStreamsDAO.execute(transaction = False)
        self.assertEqual(len(list(runStreams.keys())), 0,
                         "ERROR: there should be no new run/stream")

        self.feedStreamers()
        self.assertEqual(self.getNumFeedStreamers(), 8,
                         "ERROR: there should be 8 streamers feed")

        self.insertClosedLumiDAO.execute(binds = { 'RUN' : 176163,
                                                   'STREAM' : 'A',
                                                   'LUMI' : 1,
                                                   'INSERT_TIME' : int(time.time()),
                                                   'CLOSE_TIME' : int(time.time()),
                                                   'FILECOUNT' : 1 },
                                         transaction = False)

        self.feedStreamers()
        self.assertEqual(self.getNumFeedStreamers(), 9,
                         "ERROR: there should be 9 streamers feed")

        return

    def test01(self):
        """
        _test01_

        Test the interaction with StorageManager DB to end runs and close lumis
        for real run examples with full run and run/stream configuration

        """
        if self.dbInterfaceStorageManager == None:
            print("Your config is missing the StorageManagerDatabase section")
            print("Skipping run/lumi closing test")
            return

        RunLumiCloseoutAPI.closeRuns(self.dbInterfaceStorageManager)
        self.assertEqual(len(self.getEndedRuns()), 0,
                         "ERROR: there should be no ended runs")

        RunLumiCloseoutAPI.closeLumiSections(self.dbInterfaceStorageManager)
        self.assertEqual(len(self.getClosedLumis()), 0,
                         "ERROR: there should be no closed lumis")

        self.insertRun(176161)

        RunLumiCloseoutAPI.closeRuns(self.dbInterfaceStorageManager)
        endedRuns = self.getEndedRuns()
        self.assertEqual(list(endedRuns.keys()), [176161],
                         "ERROR: there should be 1 ended run: 176161")
        self.assertEqual(endedRuns[176161], 23,
                         "ERROR: there should be 23 lumis in run 176161")

        RunLumiCloseoutAPI.closeLumiSections(self.dbInterfaceStorageManager)
        self.assertEqual(len(self.getClosedLumis()), 0,
                         "ERROR: there should be no closed lumis")

        self.insertRunStreamLumi(176161, "A", 1)

        RunLumiCloseoutAPI.closeLumiSections(self.dbInterfaceStorageManager)
        self.assertEqual(len(self.getClosedLumis()), 0,
                         "ERROR: there should be no closed lumis")

        RunConfigAPI.configureRun(self.tier0Config, 176161,
                                  self.hltConfig,
                                  { 'process' : "HLT",
                                    'mapping' : self.referenceMapping })

        RunLumiCloseoutAPI.closeLumiSections(self.dbInterfaceStorageManager)
        self.assertEqual(len(self.getClosedLumis()), 0,
                         "ERROR: there should be no closed lumis")

        RunConfigAPI.configureRunStream(self.tier0Config, 176161, "A", self.testDir, self.dqmUploadProxy)

        RunLumiCloseoutAPI.closeLumiSections(self.dbInterfaceStorageManager)

        runStreamLumiDict = self.getClosedLumis()
        self.assertEqual(list(runStreamLumiDict.keys()), [176161],
                         "ERROR: there should be closed lumis for run 176161")
        self.assertEqual(list(runStreamLumiDict[176161].keys()), ['A'],
                         "ERROR: there should be closed lumis for run 176161 and stream A")
        self.assertEqual(sorted(runStreamLumiDict[176161]['A'].keys()), list(range(1, 24)),
                         "ERROR: there should be closed lumis for run 176161, stream A and lumi 1 to 23")

        for lumi in range(1, 24):
            self.assertEqual(runStreamLumiDict[176161]['A'][lumi], 14,
                             "ERROR: there should be 14 closed lumis for run 176161, stream A and lumi %d" % lumi)

        self.insertRunStreamLumi(176161, "HLTMON", 1)

        RunConfigAPI.configureRunStream(self.tier0Config, 176161, "HLTMON", self.testDir, self.dqmUploadProxy)

        RunLumiCloseoutAPI.closeLumiSections(self.dbInterfaceStorageManager)

        runStreamLumiDict = self.getClosedLumis()
        self.assertEqual(list(runStreamLumiDict.keys()), [176161],
                         "ERROR: there should be closed lumis for run 176161")
        self.assertEqual(sorted(runStreamLumiDict[176161].keys()), ['A', 'HLTMON'],
                         "ERROR: there should be closed lumis for run 176161 and stream A and HLTMON")
        self.assertEqual(sorted(runStreamLumiDict[176161]['A'].keys()), list(range(1, 24)),
                         "ERROR: there should be closed lumis for run 176161, stream A and lumi 1 to 23")
        self.assertEqual(sorted(runStreamLumiDict[176161]['HLTMON'].keys()), list(range(1, 24)),
                         "ERROR: there should be closed lumis for run 176161, stream HLTMON and lumi 1 to 23")

        for lumi in range(1, 24):
            self.assertEqual(runStreamLumiDict[176161]['A'][lumi], 14,
                             "ERROR: there should be 14 closed lumis for run 176161, stream A and lumi %d" % lumi)

        self.assertEqual(runStreamLumiDict[176161]['HLTMON'][1], 9,
                         "ERROR: there should be 9 closed lumis for run 176161, stream HLTMON and lumi 1")
        self.assertEqual(runStreamLumiDict[176161]['HLTMON'][2], 1,
                         "ERROR: there should be 1 closed lumis for run 176161, stream HLTMON and lumi 2")
        for lumi in range(3, 23):
            self.assertEqual(runStreamLumiDict[176161]['HLTMON'][lumi], 14,
                             "ERROR: there should be 14 closed lumis for run 176161, stream HLTMON and lumi %d" % lumi)
        self.assertEqual(runStreamLumiDict[176161]['HLTMON'][23], 6,
                         "ERROR: there should be 6 closed lumis for run 176161, stream HLTMON and lumi 23")

        return


    def test02(self):
        """
        _test02_

        Test closeout code for run/stream filesets

        """
        if self.dbInterfaceStorageManager == None:
            print("Your config is missing the StorageManagerDatabase section")
            print("Skipping run/lumi closing test")
            return

        RunLumiCloseoutAPI.closeRunStreamFilesets()
        self.assertEqual(len(self.getClosedRunStreamFilesets()), 0,
                         "ERROR: there should be no closed run/stream filesets")

        self.insertRun(176161)
        for count in range(14):
            self.insertRunStreamLumi(176161, "A", 1)

        RunConfigAPI.configureRun(self.tier0Config, 176161,
                                  self.hltConfig,
                                  { 'process' : "HLT",
                                    'mapping' : self.referenceMapping })

        RunConfigAPI.configureRunStream(self.tier0Config, 176161, "A", self.testDir, self.dqmUploadProxy)

        RunLumiCloseoutAPI.closeRuns(self.dbInterfaceStorageManager)
        RunLumiCloseoutAPI.closeLumiSections(self.dbInterfaceStorageManager)
        
        RunLumiCloseoutAPI.closeRunStreamFilesets()
        self.assertEqual(len(self.getClosedRunStreamFilesets()), 0,
                         "ERROR: there should be no closed run/stream filesets")

        self.feedStreamers()

        RunLumiCloseoutAPI.closeRunStreamFilesets()
        self.assertEqual(len(self.getClosedRunStreamFilesets()), 0,
                         "ERROR: there should be no closed run/stream filesets")

        for lumi in range(2, 24):
            for count in range(14):
                self.insertRunStreamLumi(176161, "A", lumi)

        RunLumiCloseoutAPI.closeRuns(self.dbInterfaceStorageManager)
        RunLumiCloseoutAPI.stopRuns(self.dbInterfaceStorageManager)
        RunLumiCloseoutAPI.closeLumiSections(self.dbInterfaceStorageManager)

        RunLumiCloseoutAPI.closeRunStreamFilesets()
        self.assertEqual(len(self.getClosedRunStreamFilesets()), 0,
                         "ERROR: there should be no closed run/stream filesets")

        self.feedStreamers()

        RunLumiCloseoutAPI.closeRunStreamFilesets()
        self.assertEqual(self.getClosedRunStreamFilesets(), { 176161 : 'A' },
                         "ERROR: there should be 1 closed run/stream filesets for run 176161 and stream A")


        self.assertEqual(len(self.getStreamerWorkflowsForMonitoringDAO.execute()), 1,
                         "ERROR: there should be 1 workflow to be injected to couchDB")

        self.feedCouchMonitoring()

        self.assertEqual(len(self.getStreamerWorkflowsForMonitoringDAO.execute()), 0,
                         "ERROR: there should be no workflow to be injected to couchDB")

        return


    def test03(self):
        """
        _test03_

        Test active split lumi checks

        """
        myThread = threading.currentThread()

        self.insertRun(176161)
        self.insertRunStreamLumi(176161, "A", 1)
        self.insertRunStreamLumi(176161, "A", 1)
        self.insertRunStreamLumi(176161, "A", 1)

        RunConfigAPI.configureRun(self.tier0Config, 176161,
                                  self.hltConfig,
                                  { 'process' : "HLT",
                                    'mapping' : self.referenceMapping })

        RunConfigAPI.configureRunStream(self.tier0Config, 176161, "A", self.testDir, self.dqmUploadProxy)

        self.insertClosedLumiDAO.execute(binds = { 'RUN' : 176161,
                                                   'STREAM' : 'A',
                                                   'LUMI' : 1,
                                                   'INSERT_TIME' : int(time.time()),
                                                   'CLOSE_TIME' : int(time.time()),
                                                   'FILECOUNT' : 3 },
                                         transaction = False)

        self.feedStreamers()

        subID = myThread.dbi.processData("""SELECT wmbs_subscription.id
                                            FROM run_stream_fileset_assoc
                                            INNER JOIN stream ON
                                              stream.id = run_stream_fileset_assoc.stream_id
                                            INNER JOIN wmbs_subscription ON
                                              wmbs_subscription.fileset = run_stream_fileset_assoc.fileset
                                            WHERE run_stream_fileset_assoc.run_id = 176161
                                            AND stream.name = 'A'
                                            """, transaction = False)[0].fetchall()[0][0]

        self.insertSplitLumisDAO.execute( binds = { 'SUB' : subID,
                                                    'LUMI' : 1,
                                                    'NFILES' : 3 }, conn = None, transaction = False)

        RunLumiCloseoutAPI.checkActiveSplitLumis()

        self.changeActiveLumiSplits(1)

        myThread.dbi.processData("""DELETE FROM wmbs_sub_files_available
                                    WHERE fileid = 1
                                    """, transaction = False)
        
        RunLumiCloseoutAPI.checkActiveSplitLumis()

        self.assertEqual(self.getNumActiveSplitLumis(), 1,
                         "ERROR: there should be one split lumi.")

        self.changeActiveLumiSplits(2)
        
        RunLumiCloseoutAPI.checkActiveSplitLumis()

        self.assertEqual(self.getNumActiveSplitLumis(), 1,
                         "ERROR: there should be one split lumi.")

        self.changeActiveLumiSplits(3)
        RunLumiCloseoutAPI.checkActiveSplitLumis()
        self.assertEqual(self.getNumActiveSplitLumis(), 0,
                         "ERROR: there should be no split lumi.")

        return


    def test04(self):
        """
        _test04_

        Test releasing express processing without PopConLog DB

        """
        self.insertRun(176161)

        runs = self.findNewExpressRunsDAO.execute(transaction = False)

        self.assertEqual(set(runs), set([176161]),
                         "ERROR: only run 176161 should not be express released.")

        self.releaseExpressDAO.execute(binds = { 'RUN' : 176161 }, transaction = False)

        runs = self.findNewExpressRunsDAO.execute(transaction = False)

        self.assertEqual(set(runs), set([]),
                         "ERROR: there should be no run not express released.")

        return


    def test05(self):
        """
        _test05_

        Test the interaction with PopConLog DB to release express processing

        """
        if self.getExpressReadyRunsDAO == None:
            print("Your config is missing the PopConLogDatabase section")
            print("Skipping PopConLog based express release test")
            return

        self.insertRun(176161)

        runs = self.getExpressReadyRunsDAO.execute(binds = { 'RUN' : 176161 }, transaction = False)

        self.assertEqual(set(runs), set([176161]),
                         "ERROR: only run 176161 should be ready for express release.")

        return

if __name__ == '__main__':
    unittest.main()
