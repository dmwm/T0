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
        "Requestor" : "Dirk.Hufnagel@cern.ch",

        "ScramArch" : "slc5_amd64_gcc462",
        
        # these must be overridden
        "AcquisitionEra" : None,
        "CMSSWVersion" : None,
        "ProcessingVersion" : None,
        "ProcScenario" : None,
        "GlobalTag" : None,
        "GlobalTagTransaction" : None,
        "Outputs" : None,
        "AlcaSkims" : [ "TkAlCosmics0T", "MuAlGlobalCosmics", "HcalCalHOCosmics" ],
        "DqmSequences" : [ "@common", "@jetmet" ],

        "AlcaHarvestTimeout" : None,
        "AlcaHarvestDir" : None,

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
            #output['filterName'] = "Express"
            output['moduleLabel'] = "write_%s_%s" % (output['primaryDataset'],
                                                     output['dataTier'])
            if output['dataTier'] == "ALCARECO":
                alcaPrimaryDataset = output['primaryDataset']

        # finalize splitting parameters
        mySplitArgs = self.expressSplitArgs.copy()
        mySplitArgs['algo_package'] = "T0.JobSplitting"

        expressTask = workload.newTask("Express")

        expressOutMods = self.setupProcessingTask(expressTask, taskType,
                                                  scenarioName = self.procScenario,
                                                  scenarioFunc = "expressProcessing",
                                                  scenarioArgs = { 'globalTag' : self.globalTag,
                                                                   'globalTagTransaction' : self.globalTagTransaction,
                                                                   'skims' : self.alcaSkims,
                                                                   'dqmSeq' : self.dqmSequences,
                                                                   'outputs' : self.outputs },
                                                  splitAlgo = "Express",
                                                  splitArgs = mySplitArgs,
                                                  stepType = cmsswStepType,
                                                  forceUnmerged = True)

        expressTask.setTaskType("Express")

        self.addLogCollectTask(expressTask)

        for expressOutLabel, expressOutInfo in expressOutMods.items():

            if expressOutInfo['dataTier'] == "ALCARECO":

                # finalize splitting parameters
                mySplitArgs = self.expressMergeSplitArgs.copy()
                mySplitArgs['algo_package'] = "T0.JobSplitting"

                alcaSkimTask = expressTask.addTask("%sAlcaSkim%s" % (expressTask.name(), expressOutLabel))

                alcaSkimTask.setInputReference(expressTask.getStep("cmsRun1"),
                                               outputModule = expressOutLabel)

                alcaSkimOutMods = self.setupProcessingTask(alcaSkimTask, taskType,
                                                           scenarioName = self.procScenario,
                                                           scenarioFunc = "alcaSkim",
                                                           scenarioArgs = { 'globalTag' : self.globalTag,
                                                                            'globalTagTransaction' : self.globalTagTransaction,
                                                                            'skims' : self.alcaSkims,
                                                                            'primaryDataset' : alcaPrimaryDataset },
                                                           splitAlgo = "ExpressMerge",
                                                           splitArgs = mySplitArgs,
                                                           stepType = cmsswStepType,
                                                           forceMerged = True)

                alcaSkimTask.setTaskType("Express")

                self.addLogCollectTask(alcaSkimTask, taskName = "%s%sAlcaSkimLogCollect" % (expressTask.name(), expressOutLabel))
                self.addCleanupTask(expressTask, expressOutLabel)

                for alcaSkimOutLabel, alcaSkimOutInfo in alcaSkimOutMods.items():

                    if alcaSkimOutInfo['dataTier'] == "ALCAPROMPT" and self.alcaHarvestDir != None:

                        harvestTask = self.addAlcaHarvestTask(alcaSkimTask, alcaSkimOutLabel,
                                                              condOutLabel = self.alcaHarvestOutLabel,
                                                              condUploadDir = self.alcaHarvestDir,
                                                              uploadProxy = self.dqmUploadProxy,
                                                              doLogCollect = True)

                        self.addConditionTask(harvestTask, self.alcaHarvestOutLabel)

            else:

                mergeTask = self.addExpressMergeTask(expressTask, expressOutLabel)

                if expressOutInfo['dataTier'] in [ "DQM", "DQMROOT" ]:

                    self.addDQMHarvestTask(mergeTask, "Merged",
                                           uploadProxy = self.dqmUploadProxy,
                                           periodic_harvest_interval = 20 * 60,
                                           doLogCollect = True)

        return workload

    def addExpressMergeTask(self, parentTask, parentOutputModuleName):
        """
        _addExpressMergeTask_

        Create an expressmerge task for files produced by the parent task

        """
        # finalize splitting parameters
        mySplitArgs = self.expressMergeSplitArgs.copy()
        mySplitArgs['algo_package'] = "T0.JobSplitting"

        parentTaskCmssw = parentTask.getStep("cmsRun1")
        parentOutputModule = parentTaskCmssw.getOutputModule(parentOutputModuleName)

        mergeTask = parentTask.addTask("%sMerge%s" % (parentTask.name(), parentOutputModuleName))

        mergeTask.setInputReference(parentTaskCmssw, outputModule = parentOutputModuleName)

        self.addDashboardMonitoring(mergeTask)
        mergeTaskCmssw = mergeTask.makeStep("cmsRun1")
        mergeTaskCmssw.setStepType("CMSSW")

        mergeTaskStageOut = mergeTaskCmssw.addStep("stageOut1")
        mergeTaskStageOut.setStepType("StageOut")
        mergeTaskLogArch = mergeTaskCmssw.addStep("logArch1")
        mergeTaskLogArch.setStepType("LogArchive")

        mergeTask.setTaskLogBaseLFN(self.unmergedLFNBase)

        self.addLogCollectTask(mergeTask, taskName = "%s%sMergeLogCollect" % (parentTask.name(), parentOutputModuleName))

        mergeTask.applyTemplates()
        mergeTask.setTaskPriority(self.priority + 5)

        mergeTaskCmsswHelper = mergeTaskCmssw.getTypeHelper()
        mergeTaskStageHelper = mergeTaskStageOut.getTypeHelper()

        mergeTaskCmsswHelper.cmsswSetup(self.frameworkVersion, softwareEnvironment = "",
                                        scramArch = self.scramArch)

        mergeTaskCmsswHelper.setErrorDestinationStep(stepName = mergeTaskLogArch.name())
        mergeTaskCmsswHelper.setGlobalTag(self.globalTag)
        mergeTaskCmsswHelper.setOverrideCatalog(self.overrideCatalog)

        #mergeTaskStageHelper.setMinMergeSize(0, 0)

        mergeTask.setTaskType("Merge")

        # DQM is handled differently
        #  merging does not increase size
        #                => disable size limits
        #  only harvest every 15 min
        #                => higher limits for latency (disabled for now)
        dqm_format = getattr(parentOutputModule, "dataTier") == "DQM"
        if dqm_format:
            mySplitArgs['maxInputSize'] *= 100

        mergeTask.setSplittingAlgorithm("ExpressMerge",
                                        **mySplitArgs)
        mergeTaskCmsswHelper.setDataProcessingConfig(self.procScenario, "merge", dqm_format = dqm_format)

        self.addOutputModule(mergeTask, "Merged",
                             primaryDataset = getattr(parentOutputModule, "primaryDataset"),
                             dataTier = getattr(parentOutputModule, "dataTier"),
                             filterName = getattr(parentOutputModule, "filterName"),
                             forceMerged = True)

        self.addCleanupTask(parentTask, parentOutputModuleName)

        return mergeTask

    def addAlcaHarvestTask(self, parentTask, parentOutputModuleName,
                           condOutLabel, condUploadDir, uploadProxy,
                           parentStepName = "cmsRun1", doLogCollect = True):
        """
        _addAlcaHarvestTask_

        Create an Alca harvest task to harvest the files produces by the parent task.
        """
        # finalize splitting parameters
        mySplitArgs = {}
        mySplitArgs['algo_package'] = "T0.JobSplitting"
        mySplitArgs['runNumber'] = self.runNumber
        mySplitArgs['timeout'] = self.alcaHarvestTimeout

        harvestTask = parentTask.addTask("%sAlcaHarvest%s" % (parentTask.name(), parentOutputModuleName))
        self.addDashboardMonitoring(harvestTask)
        harvestTaskCmssw = harvestTask.makeStep("cmsRun1")
        harvestTaskCmssw.setStepType("CMSSW")

        harvestTaskCondition = harvestTaskCmssw.addStep("condition1")
        harvestTaskCondition.setStepType("AlcaHarvest")
        harvestTaskUpload = harvestTaskCmssw.addStep("upload1")
        harvestTaskUpload.setStepType("DQMUpload")
        harvestTaskLogArch = harvestTaskCmssw.addStep("logArch1")
        harvestTaskLogArch.setStepType("LogArchive")

        harvestTask.setTaskLogBaseLFN(self.unmergedLFNBase)
        if doLogCollect:
            self.addLogCollectTask(harvestTask, taskName = "%s%sAlcaHarvestLogCollect" % (parentTask.name(), parentOutputModuleName))

        harvestTask.setTaskType("Harvesting")
        harvestTask.applyTemplates()
        harvestTask.setTaskPriority(self.priority + 5)

        harvestTaskCmsswHelper = harvestTaskCmssw.getTypeHelper()
        harvestTaskCmsswHelper.cmsswSetup(self.frameworkVersion, softwareEnvironment = "",
                                          scramArch = self.scramArch)

        harvestTaskCmsswHelper.setErrorDestinationStep(stepName = harvestTaskLogArch.name())
        harvestTaskCmsswHelper.setGlobalTag(self.globalTag)
        harvestTaskCmsswHelper.setOverrideCatalog(self.overrideCatalog)

        harvestTaskCmsswHelper.setUserLFNBase("/")

        parentTaskCmssw = parentTask.getStep(parentStepName)
        parentOutputModule = parentTaskCmssw.getOutputModule(parentOutputModuleName)

        harvestTask.setInputReference(parentTaskCmssw, outputModule = parentOutputModuleName)

        harvestTask.setSplittingAlgorithm("AlcaHarvest",
                                          **mySplitArgs)

        harvestTaskCmsswHelper.setDataProcessingConfig(self.procScenario, "alcaHarvesting",
                                                       globalTag = self.globalTag,
                                                       datasetName = "/%s/%s/%s" % (getattr(parentOutputModule, "primaryDataset"),
                                                                                    getattr(parentOutputModule, "processedDataset"),
                                                                                    getattr(parentOutputModule, "dataTier")),
                                                       runNumber = self.runNumber)

        harvestTaskConditionHelper = harvestTaskCondition.getTypeHelper()
        harvestTaskConditionHelper.setRunNumber(self.runNumber)
        harvestTaskConditionHelper.setConditionOutputLabel(condOutLabel)
        harvestTaskConditionHelper.setConditionDir(condUploadDir)

        self.addOutputModule(harvestTask, condOutLabel,
                             primaryDataset = getattr(parentOutputModule, "primaryDataset"),
                             dataTier = getattr(parentOutputModule, "dataTier"),
                             filterName = getattr(parentOutputModule, "filterName"))

        harvestTaskUploadHelper = harvestTaskUpload.getTypeHelper()
        harvestTaskUploadHelper.setProxyFile(uploadProxy)

        return harvestTask

    def addConditionTask(self, parentTask, parentOutputModuleName):
        """
        _addConditionTask_

        Does not actually produce any jobs
        The job splitter is custom and just forwards information
        into T0AST specific data structures, the actual upload
        of the conditions to the DropBox is handled in a separate
        Tier0 component.
        
        """
        # finalize splitting parameters
        mySplitArgs = {}
        mySplitArgs['algo_package'] = "T0.JobSplitting"
        mySplitArgs['runNumber'] = self.runNumber
        mySplitArgs['streamName'] = self.streamName

        parentTaskCmssw = parentTask.getStep("cmsRun1")
        parentOutputModule = parentTaskCmssw.getOutputModule(parentOutputModuleName)

        conditionTask = parentTask.addTask("%sCondition%s" % (parentTask.name(), parentOutputModuleName))

        # this is complete bogus, but other code can't deal with a task with no steps
        conditionTaskBogus = conditionTask.makeStep("bogus")
        conditionTaskBogus.setStepType("DQMUpload")

        conditionTask.setInputReference(parentTaskCmssw, outputModule = parentOutputModuleName)

        conditionTask.applyTemplates()
        conditionTask.setTaskPriority(self.priority + 5)

        conditionTask.setTaskType("Harvesting")

        conditionTask.setSplittingAlgorithm("Condition",
                                            **mySplitArgs)

        return

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
        self.dqmSequences = arguments['DqmSequences']
        self.outputs = arguments['Outputs']
        self.dqmUploadProxy = arguments['DQMUploadProxy']
        self.alcaHarvestTimeout = arguments['AlcaHarvestTimeout']
        self.alcaHarvestDir = arguments['AlcaHarvestDir']
        self.streamName = arguments['StreamName']

        # job splitting parameters (also required parameters)
        self.expressSplitArgs = {}
        self.expressSplitArgs['maxInputEvents'] = arguments['MaxInputEvents']
        self.expressMergeSplitArgs = {}
        self.expressMergeSplitArgs['maxInputSize'] = arguments['MaxInputSize']
        self.expressMergeSplitArgs['maxInputFiles'] = arguments['MaxInputFiles']
        self.expressMergeSplitArgs['maxLatency'] = arguments['MaxLatency']

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

        # fixed parameters that are used in various places
        self.alcaHarvestOutLabel = "Sqlite"

        return self.buildWorkload()

def expressWorkload(workloadName, arguments):
    """
    _expressWorkload_

    Instantiate the ExpressWorkflowFactory and have
    it generate a workload for the given parameters.
    """
    myExpressFactory = ExpressWorkloadFactory()
    return myExpressFactory(workloadName, arguments)
