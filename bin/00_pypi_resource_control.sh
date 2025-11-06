#!/bin/bash

#Settings for using T0_CH_CERN_Disk
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --cms-name=T2_CH_CERN --pnn=T0_CH_CERN_Disk --ce-name=T2_CH_CERN --pending-slots=25000 --running-slots=52000 --plugin=SimpleCondorPlugin
manage execute-agent wmagent-resource-control --site-name=T0_CH_CERN_Disk --cms-name=T0_CH_CERN_Disk --pnn=T2_CH_CERN --ce-name=T0_CH_CERN_Disk --pending-slots=25000 --running-slots=52000 --plugin=SimpleCondorPlugin
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Processing --pending-slots=10000 --running-slots=25000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Merge --pending-slots=1000 --running-slots=1000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Cleanup --pending-slots=1000 --running-slots=1000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=LogCollect --pending-slots=1000 --running-slots=1000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Skim --pending-slots=1 --running-slots=1
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Production --pending-slots=1 --running-slots=1
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Harvesting --pending-slots=1000 --running-slots=1000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Express --pending-slots=4000 --running-slots=8000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Repack --pending-slots=7000 --running-slots=15000

# Settings for using T2_CH_CERN_P5 and T1 sites (PromptReco)
# Values set to 0 because we want to control job submission amount
# Jobs are then set to run at the sites with condor commands and cronjobs
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --cms-name=T2_CH_CERN_P5 --pnn=T2_CH_CERN_P5 --ce-name=T2_CH_CERN_P5 --pending-slots=0 --running-slots=0 --plugin=SimpleCondorPlugin
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Processing --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Merge --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Cleanup --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=LogCollect --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Skim --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Production --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Harvesting --pending-slots=0 --running-slots=0

manage execute-agent wmagent-resource-control --site-name=T1_DE_KIT --cms-name=T1_DE_KIT --pnn=T1_DE_KIT --ce-name=T1_DE_KIT --pending-slots=0 --running-slots=0 --plugin=SimpleCondorPlugin
manage execute-agent wmagent-resource-control --site-name=T1_DE_KIT --task-type=Processing --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_DE_KIT --task-type=Merge --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_DE_KIT --task-type=Cleanup --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_DE_KIT --task-type=LogCollect --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_DE_KIT --task-type=Skim --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_DE_KIT --task-type=Production --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_DE_KIT --task-type=Harvesting --pending-slots=0 --running-slots=0

manage execute-agent wmagent-resource-control --site-name=T1_UK_RAL --cms-name=T1_UK_RAL --pnn=T1_UK_RAL --ce-name=T1_UK_RAL --pending-slots=0 --running-slots=0 --plugin=SimpleCondorPlugin
manage execute-agent wmagent-resource-control --site-name=T1_UK_RAL --task-type=Processing --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_UK_RAL --task-type=Merge --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_UK_RAL --task-type=Cleanup --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_UK_RAL --task-type=LogCollect --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_UK_RAL --task-type=Skim --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_UK_RAL --task-type=Production --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_UK_RAL --task-type=Harvesting --pending-slots=0 --running-slots=0

manage execute-agent wmagent-resource-control --site-name=T1_FR_CCIN2P3 --cms-name=T1_FR_CCIN2P3 --pnn=T1_FR_CCIN2P3 --ce-name=T1_FR_CCIN2P3 --pending-slots=0 --running-slots=0 --plugin=SimpleCondorPlugin
manage execute-agent wmagent-resource-control --site-name=T1_FR_CCIN2P3 --task-type=Processing --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_FR_CCIN2P3 --task-type=Merge --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_FR_CCIN2P3 --task-type=Cleanup --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_FR_CCIN2P3 --task-type=LogCollect --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_FR_CCIN2P3 --task-type=Skim --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_FR_CCIN2P3 --task-type=Production --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_FR_CCIN2P3 --task-type=Harvesting --pending-slots=0 --running-slots=0

manage execute-agent wmagent-resource-control --site-name=T1_US_FNAL --cms-name=T1_US_FNAL --pnn=T1_US_FNAL --ce-name=T1_US_FNAL --pending-slots=0 --running-slots=0 --plugin=SimpleCondorPlugin
manage execute-agent wmagent-resource-control --site-name=T1_US_FNAL --task-type=Processing --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_US_FNAL --task-type=Merge --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_US_FNAL --task-type=Cleanup --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_US_FNAL --task-type=LogCollect --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_US_FNAL --task-type=Skim --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_US_FNAL --task-type=Production --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_US_FNAL --task-type=Harvesting --pending-slots=0 --running-slots=0

manage execute-agent wmagent-resource-control --site-name=T1_ES_PIC --cms-name=T1_ES_PIC --pnn=T1_ES_PIC --ce-name=T1_ES_PIC --pending-slots=0 --running-slots=0 --plugin=SimpleCondorPlugin
manage execute-agent wmagent-resource-control --site-name=T1_ES_PIC --task-type=Processing --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_ES_PIC --task-type=Merge --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_ES_PIC --task-type=Cleanup --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_ES_PIC --task-type=LogCollect --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_ES_PIC --task-type=Skim --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_ES_PIC --task-type=Production --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_ES_PIC --task-type=Harvesting --pending-slots=0 --running-slots=0

manage execute-agent wmagent-resource-control --site-name=T1_IT_CNAF --cms-name=T1_IT_CNAF --pnn=T1_IT_CNAF --ce-name=T1_IT_CNAF --pending-slots=0 --running-slots=0 --plugin=SimpleCondorPlugin
manage execute-agent wmagent-resource-control --site-name=T1_IT_CNAF --task-type=Processing --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_IT_CNAF --task-type=Merge --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_IT_CNAF --task-type=Cleanup --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_IT_CNAF --task-type=LogCollect --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_IT_CNAF --task-type=Skim --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_IT_CNAF --task-type=Production --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_IT_CNAF --task-type=Harvesting --pending-slots=0 --running-slots=0

manage execute-agent wmagent-resource-control --site-name=T1_RU_JINR --cms-name=T1_RU_JINR --pnn=T1_RU_JINR --ce-name=T1_RU_JINR --pending-slots=0 --running-slots=0 --plugin=SimpleCondorPlugin
manage execute-agent wmagent-resource-control --site-name=T1_RU_JINR --task-type=Processing --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_RU_JINR --task-type=Merge --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_RU_JINR --task-type=Cleanup --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_RU_JINR --task-type=LogCollect --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_RU_JINR --task-type=Skim --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_RU_JINR --task-type=Production --pending-slots=0 --running-slots=0
manage execute-agent wmagent-resource-control --site-name=T1_RU_JINR --task-type=Harvesting --pending-slots=0 --running-slots=0