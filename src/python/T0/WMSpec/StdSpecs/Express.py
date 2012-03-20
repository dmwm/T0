"""
_Express_

Express workflow

express processing -> FEVT/RAW/RECO/whatever -> express merge
                      (supports multiple output with different primary datasets)
                   -> ALCARECO -> alca skimming / merging -> ALCARECO
                                                          -> ALCAPROMPT -> end of run alca harvesting -> sqlite -> dropbox upload
                   -> DQM -> merge -> DQM -> periodic dqm harvesting
                                          -> end of run dqm harvesting

"""

import os

from WMCore.WMSpec.StdSpecs.StdBase import StdBase

def getTestArguments():
    """
    _getTestArguments_

    This should be where the default REQUIRED arguments go
    This serves as documentation for what is currently required 
    by the standard Express workload in importable format.

    NOTE: These are test values.  If used in real workflows they
    will cause everything to crash/die/break, and we will be forced
    to hunt you down and kill you.
    """
    arguments = {
        "AcquisitionEra" : "Tier0Testing",
        "Requestor" : "Dirk.Hufnagel@cern.ch",

        "ScramArch" : "slc5_amd64_gcc462",
        
        # these must be overridden
        "CMSSWVersion" : None,
        "ProcessingVersion" : None,
        "ProcScenario" : None,
        "GlobalTag" : None,
        "GlobalTagTransaction" : None,
        "Outputs" : None,
        "AlcaSkims" : None,

        # optional for now
        "Multicore" : None,
        }

    return arguments

class ExpressWorkloadFactory(StdBase):
    """
    _ExpressWorkloadFactory_

    Stamp out Express workflows.
    """
    def __init__(self):
        StdBase.__init__(self)
        self.multicore = False
        self.multicoreNCores = 1
        return

    def buildWorkload(self):
        """
        _buildWorkload_

        Build the workload given all of the input parameters.

        Not that there will be LogCollect tasks created for each processing
        task and Cleanup tasks created for each merge task.

        """
        workload = self.createWorkload()
        workload.setDashboardActivity("tier0")

        cmsswStepType = "CMSSW"
        taskType = "Processing"
        if self.multicore:
            taskType = "MultiProcessing"

        # complete output configuration
        # figure out alca primary dataset
        alcaPrimaryDataset = None
        for output in self.outputs:
            output['filterName'] = "Express"
            output['moduleLabel'] = "write_%s_%s" % (output['primaryDataset'],
                                                     output['dataTier'])
            if output['dataTier'] == "ALCARECO":
                alcaPrimaryDataset = output['primaryDataset']

        #
        # different datasets for different outputs, how to handle ?
        # self.inputDataset replacement
        #
        expressTask = workload.newTask("Express")
        expressOutMods = self.setupProcessingTask(expressTask, taskType,
                                                  scenarioName = self.procScenario,
                                                  scenarioFunc = "expressProcessing",
                                                  scenarioArgs = { 'globalTag' : self.globalTag,
                                                                   'globalTagTransaction' : self.globalTagTransaction,
                                                                   'skims' : self.alcaSkims,
                                                                   'outputs' : self.outputs },
                                                  splitAlgo = "Express",
                                                  splitArgs = { 'algo_package' : "T0.JobSplitting" },
                                                  stepType = cmsswStepType)
        self.addLogCollectTask(expressTask)

        for expressOutLabel, expressOutInfo in expressOutMods.items():
            if expressOutInfo['dataTier'] == "ALCARECO":
                alcaTask = expressTask.addTask("AlcaSkim")
                alcaOutMods = self.setupProcessingTask(alcaTask, taskType,
                                                       inputStep = expressTask.getStep("cmsRun1"),
                                                       inputModule = expressOutLabel,
                                                       scenarioName = self.procScenario,
                                                       scenarioFunc = "alcaSkim",
                                                       scenarioArgs = { 'globalTag' : self.globalTag,
                                                                        'globalTagTransaction' : self.globalTagTransaction,
                                                                        'skims' : self.alcaSkims,
                                                                        'primaryDataset' : alcaPrimaryDataset },
                                                       splitAlgo = "FileBased",
                                                       splitArgs = {},
                                                       stepType = cmsswStepType)
##                 for alcaOutLabel in alcaOutMods.keys():
##                     self.addMergeTask(alcaTask,
##                                       "FileBased",
##                                       alcaOutLabel)
##             else:
##                 self.addMergeTask(expressTask,
##                                   "FileBased",
##                                   expressOutLabel)

        return workload

    def __call__(self, workloadName, arguments):
        """
        _call_

        Create a Express workload with the given parameters.
        """
        StdBase.__call__(self, workloadName, arguments)

        # Required parameters that must be specified by the Requestor.
        self.frameworkVersion = arguments["CMSSWVersion"]
        self.globalTag = arguments["GlobalTag"]
	self.globalTagTransaction = arguments["GlobalTagTransaction"]
        self.procScenario = arguments['ProcScenario']
        self.alcaSkims = arguments['AlcaSkims']
        self.outputs = arguments['Outputs']

        if arguments.has_key("Multicore"):
            numCores = arguments.get("Multicore")
            if numCores == None or numCores == "":
                self.multicore = False
            elif numCores == "auto":
                self.multicore = True
                self.multicoreNCores = "auto"
            else:
                self.multicore = True
                self.multicoreNCores = numCores

        # Optional arguments that default to something reasonable.
        self.dbsUrl = arguments.get("DbsUrl", "http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet")
        self.blockBlacklist = arguments.get("BlockBlacklist", [])
        self.blockWhitelist = arguments.get("BlockWhitelist", [])
        self.runBlacklist = arguments.get("RunBlacklist", [])
        self.runWhitelist = arguments.get("RunWhitelist", [])
        self.emulation = arguments.get("Emulation", False)

        return self.buildWorkload()

def expressWorkload(workloadName, arguments):
    """
    _expressWorkload_

    Instantiate the ExpressWorkflowFactory and have
    it generate a workload for the given parameters.
    """
    myExpressFactory = ExpressWorkloadFactory()
    return myExpressFactory(workloadName, arguments)
