"""
_Repack_

Repack workflow

repacking -> RAW -> optional merge
             (supports multiple output with different primary datasets)

"""

import os

from WMCore.WMSpec.StdSpecs.StdBase import StdBase

def getTestArguments():
    """
    _getTestArguments_

    This should be where the default REQUIRED arguments go
    This serves as documentation for what is currently required 
    by the standard Repack workload in importable format.

    NOTE: These are test values.  If used in real workflows they
    will cause everything to crash/die/break, and we will be forced
    to hunt you down and kill you.
    """
    arguments = {
        "AcquisitionEra": "Tier0Commissioning11",
        "Requestor": "Dirk.Hufnagel@cern.ch",
        "CMSSWVersion": "CMSSW_4_4_2",
        "ScramArch": "slc5_amd64_gcc434",
        "ProcessingVersion": "v1",
        
        "CouchURL": os.environ.get("COUCHURL", None),
        "CouchDBName": "scf_wmagent_configcache",
        
        "ProcScenario": "cosmics",
        #"ProcConfigCacheID": "03da10e20c7b98c79f9d6a5c8900f83b",

        "GlobalTag" : None,

        "Multicore" : None,
        }

    return arguments

class RepackWorkloadFactory(StdBase):
    """
    _RepackWorkloadFactory_

    Stamp out Repack workflows.
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
        # setup repack processing task
        #
        repackTask = workload.newTask("Repack")
        self.addDashboardMonitoring(repackTask)

        repackTaskCmssw = repackTask.makeStep("cmsRun1")
        repackTaskCmssw.setStepType(cmsswStepType)
        repackTaskStageOut = repackTaskCmssw.addStep("stageOut1")
        repackTaskStageOut.setStepType("StageOut")
        repackTaskStageOut.setUserDN(None)
        repackTaskStageOut.setAsyncDest(None)
        repackTaskStageOut.setPublishName(None)
        repackTaskStageOut.setUserRoleAndGroup(self.owner_vogroup, self.owner_vorole)
        repackTaskLogArch = repackTaskCmssw.addStep("logArch1")
        repackTaskLogArch.setStepType("LogArchive")
        repackTask.applyTemplates()
        repackTask.setTaskPriority(self.priority)

        repackTask.setTaskLogBaseLFN(self.unmergedLFNBase)
        repackTask.setSiteWhitelist(self.siteWhitelist)
        repackTask.setSiteBlacklist(self.siteBlacklist)

        newSplitArgs = { 'algo_package' : "T0.JobSplitting" }
        for argName in self.procJobSplitArgs.keys():
            newSplitArgs[str(argName)] = self.procJobSplitArgs[argName]

        repackTask.setSplittingAlgorithm(self.procJobSplitAlgo, **newSplitArgs)
        repackTask.setTaskType(taskType)

        repackTaskCmsswHelper = repackTaskCmssw.getTypeHelper()
        repackTaskCmsswHelper.setUserSandbox(None)
        repackTaskCmsswHelper.setUserFiles(None)
        repackTaskCmsswHelper.setGlobalTag(self.globalTag)
        repackTaskCmsswHelper.setErrorDestinationStep(stepName = repackTaskLogArch.name())
        repackTaskCmsswHelper.cmsswSetup(self.frameworkVersion,
                                          softwareEnvironment = "",
                                          scramArch = self.scramArch)

        repackTaskCmsswHelper.setDataProcessingConfig(self.procScenario, "expressProcessing",
                                                       globalTag = self.globalTag,
                                                       writeTiers = [ 'RAW' ]
                                                       )

        self.addOutputModule(repackTask,
                             "write_FEVT",
                             "FakePrimaryDataset",
                             "FEVT",
                             None)

        self.addLogCollectTask(repackTask)
        if self.multicore:
            cmsswStep = procTask.getStep("cmsRun1")
            multicoreHelper = cmsswStep.getTypeHelper()
            multicoreHelper.setMulticoreCores(self.multicoreNCores)

        return workload

    def __call__(self, workloadName, arguments):
        """
        _call_

        Create a Repack workload with the given parameters.
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
        self.procJobSplitAlgo  = arguments.get("StdJobSplitAlgo", "Repack")
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
        if schema.has_key('ProcConfigCacheID') and schema.has_key('CouchURL') and schema.has_key('CouchDBName'):
            outMod = self.validateConfigCacheExists(configID = schema['ProcConfigCacheID'],
                                                    couchURL = schema["CouchURL"],
                                                    couchDBName = schema["CouchDBName"],
                                                    getOutputModules = True)
        elif not schema.has_key('ProcScenario'):
            self.raiseValidationException(msg = "No Scenario or Config in Processing Request!")
            
        return

def repackWorkload(workloadName, arguments):
    """
    _repackWorkload_

    Instantiate the RepackWorkflowFactory and have
    it generate a workload for the given parameters.
    """
    myRepackFactory = RepackWorkloadFactory()
    return myRepackFactory(workloadName, arguments)
