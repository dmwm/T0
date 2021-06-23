###
### Configuration file for Container Replay tests
###

#T0_VERSION specifies which image tag to use
T0_VERSION=2.2.3

#WMC_PR specifies a list of WMCore Pull Request to be tested
#WMC_PR=""
WMC_PR="10344"


#If REPLAY_TEST=1, specify the type of run you want to test picking one of the following options
#	MWGR				Latest MWGR replay test
#	HIColissions2018	Heavy Ion run from 2018		
#	ppColissions2018	Proton-Proton run from 2018
#	ThisPR				Use the replay configuration specified in this PR
#
RUN_TYPE=ThisPR
