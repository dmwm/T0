#!/bin/bash

#Settings for using T0_CH_CERN_Disk
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --cms-name=T2_CH_CERN --pnn=T0_CH_CERN_Disk --ce-name=T2_CH_CERN --pending-slots=20000 --running-slots=20000 --plugin=SimpleCondorPlugin
manage execute-agent wmagent-resource-control --site-name=T0_CH_CERN_Disk --cms-name=T0_CH_CERN_Disk --pnn=T2_CH_CERN --ce-name=T0_CH_CERN_Disk --pending-slots=20000 --running-slots=20000 --plugin=SimpleCondorPlugin
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Processing --pending-slots=10000 --running-slots=10000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Merge --pending-slots=1000 --running-slots=1000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Cleanup --pending-slots=1000 --running-slots=1000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=LogCollect --pending-slots=1000 --running-slots=1000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Skim --pending-slots=1 --running-slots=1
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Production --pending-slots=1 --running-slots=1
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Harvesting --pending-slots=1000 --running-slots=1000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Express --pending-slots=3000 --running-slots=3000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN --task-type=Repack --pending-slots=5000 --running-slots=5000

#Settings for using T2_CH_CERN_P5 (PromptReco)
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --cms-name=T2_CH_CERN_P5 --pnn=T2_CH_CERN_P5 --ce-name=T2_CH_CERN_P5 --pending-slots=20000 --running-slots=20000 --plugin=SimpleCondorPlugin
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Processing --pending-slots=10000 --running-slots=10000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Merge --pending-slots=1000 --running-slots=1000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Cleanup --pending-slots=1000 --running-slots=1000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=LogCollect --pending-slots=1000 --running-slots=1000
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Skim --pending-slots=1 --running-slots=1
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Production --pending-slots=1 --running-slots=1
manage execute-agent wmagent-resource-control --site-name=T2_CH_CERN_P5 --task-type=Harvesting --pending-slots=1000 --running-slots=1000

#t0 --resource-control=T1_ES_PIC
#t0 --resource-control=T1_I_CNAF
#t0 --resource-control=T1_DE_KIT
#t0 --resource-control=T1_UK_RAL
#t0 --resource-control=T1_FR_CCIN2P3