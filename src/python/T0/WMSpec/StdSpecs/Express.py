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
        "AcquisitionEra": "Tier0Commissioning11",
        "Requestor": "Dirk.Hufnagel@cern.ch",

        "ScramArch": "slc5_amd64_gcc434",
        
        "CouchURL": os.environ.get("COUCHURL", None),
        "CouchDBName": "scf_wmagent_configcache",

        # these must be overridden
        "CMSSWVersion": None,
        "ProcessingVersion": None,
        "ProcScenario": None,
        "GlobalTag" : None,

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

        Build the workload given all of the input parameters.  At the very least
        this will create a processing task and merge tasks for all the outputs
        of the processing task.

        Not that there will be LogCollect tasks created for each processing
        task and Cleanup tasks created for each merge task.

        """
        workload = self.createWorkload()
        workload.setDashboardActivity("tier0")

        cmsswStepType = "CMSSW"
        taskType = "Processing"
        if self.multicore:
            cmsswStepType = "MulticoreCMSSW"
            taskType = "MultiProcessing"

        #
        # setup express processing task
        #
        expressTask = workload.newTask("Express")
        self.addDashboardMonitoring(expressTask)

        expressTaskCmssw = expressTask.makeStep("cmsRun1")
        expressTaskCmssw.setStepType(cmsswStepType)
        expressTaskStageOut = expressTaskCmssw.addStep("stageOut1")
        expressTaskStageOut.setStepType("StageOut")
        expressTaskStageOut.setUserDN(None)
        expressTaskStageOut.setAsyncDest(None)
        expressTaskStageOut.setUserRoleAndGroup(self.owner_vogroup, self.owner_vorole)
        expressTaskLogArch = expressTaskCmssw.addStep("logArch1")
        expressTaskLogArch.setStepType("LogArchive")
        expressTask.applyTemplates()
        expressTask.setTaskPriority(self.priority)

        expressTask.setTaskLogBaseLFN(self.unmergedLFNBase)
        expressTask.setSiteWhitelist(self.siteWhitelist)
        expressTask.setSiteBlacklist(self.siteBlacklist)

        newSplitArgs = { 'algo_package' : "T0.JobSplitting" }
        for argName in self.procJobSplitArgs.keys():
            newSplitArgs[str(argName)] = self.procJobSplitArgs[argName]

        expressTask.setSplittingAlgorithm(self.procJobSplitAlgo, **newSplitArgs)
        expressTask.setTaskType(taskType)

        expressTaskCmsswHelper = expressTaskCmssw.getTypeHelper()
        expressTaskCmsswHelper.setUserSandbox(None)
        expressTaskCmsswHelper.setUserFiles(None)
        expressTaskCmsswHelper.setGlobalTag(self.globalTag)
        expressTaskCmsswHelper.setErrorDestinationStep(stepName = expressTaskLogArch.name())
        expressTaskCmsswHelper.cmsswSetup(self.frameworkVersion,
                                          softwareEnvironment = "",
                                          scramArch = self.scramArch)

        expressTaskCmsswHelper.setDataProcessingConfig(self.procScenario, "expressProcessing",
                                                       globalTag = self.globalTag,
                                                       writeTiers = [ 'FEVT' ]
                                                       )

        self.addOutputModule(expressTask,
                             "outputFEVTFEVT",
                             "FakePrimaryDataset",
                             "FEVT",
                             None)

        self.addLogCollectTask(expressTask)
        if self.multicore:
            cmsswStep = procTask.getStep("cmsRun1")
            multicoreHelper = cmsswStep.getTypeHelper()
            multicoreHelper.setMulticoreCores(self.multicoreNCores)

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

        # The CouchURL and name of the ConfigCache database must be passed in
        # by the ReqMgr or whatever is creating this workflow.
        self.couchURL = arguments["CouchURL"]
        self.couchDBName = arguments["CouchDBName"]        

        # One of these parameters must be set.
        if arguments.has_key("ProdConfigCacheID"):
            self.procConfigCacheID = arguments["ProdConfigCacheID"]
        else:
            self.procConfigCacheID = arguments.get("ProcConfigCacheID", None)

        if arguments.has_key("Scenario"):
            self.procScenario = arguments.get("Scenario", None)
        else:
            self.procScenario = arguments.get("ProcScenario", None)

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

        # These are mostly place holders because the job splitting algo and
        # parameters will be updated after the workflow has been created.
        self.procJobSplitAlgo  = arguments.get("StdJobSplitAlgo", "Express")
        self.procJobSplitArgs  = arguments.get("StdJobSplitArgs", {})

        return self.buildWorkload()

    def validateSchema(self, schema):
        """
        _validateSchema_
        
        Check for required fields
        """
        requiredFields = ["CMSSWVersion", "ScramArch", "GlobalTag"]
        self.requireValidateFields(fields = requiredFields,
                                   schema = schema,
                                   validate = False)
        if not schema.has_key('ProcScenario'):
            self.raiseValidationException(msg = "No Scenario defined!")
            
        return

def expressWorkload(workloadName, arguments):
    """
    _expressWorkload_

    Instantiate the ExpressWorkflowFactory and have
    it generate a workload for the given parameters.
    """
    myExpressFactory = ExpressWorkloadFactory()
    return myExpressFactory(workloadName, arguments)
