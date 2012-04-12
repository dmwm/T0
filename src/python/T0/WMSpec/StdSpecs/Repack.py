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
        "AcquisitionEra": "Tier0Testing",
        "Requestor": "Dirk.Hufnagel@cern.ch",

        "ScramArch": "slc5_amd64_gcc462",

        # needed, but ultimately not used for anything
        "ProcScenario": "not_used_but_cannot_be_none",

        # these must be overridden
        "CMSSWVersion": None,
        "ProcessingVersion": None,
        "Outputs" : None,

        # optional for now
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
            taskType = "MultiProcessing"

        # complete output configuration
        for output in self.outputs:
            output['moduleLabel'] = "write_%s_%s" % (output['primaryDataset'],
                                                     output['dataTier'])

        repackTask = workload.newTask("Repack")
        repackOutMods = self.setupProcessingTask(repackTask, taskType,
                                                 scenarioName = self.procScenario,
                                                 scenarioFunc = "repack",
                                                 scenarioArgs = { 'outputs' : self.outputs },
                                                 splitAlgo = "Repack",
                                                 splitArgs = { 'algo_package' : "T0.JobSplitting" },
                                                 stepType = cmsswStepType)

        for repackOutLabel, repackOutInfo in repackOutMods.items():
            self.addMergeTask(repackTask, "Repack", repackOutLabel,
                              "cmsRun1", doLogCollect = False)

        return workload

    def __call__(self, workloadName, arguments):
        """
        _call_

        Create a Repack workload with the given parameters.
        """
        StdBase.__call__(self, workloadName, arguments)

        # Required parameters that must be specified by the Requestor.
        self.frameworkVersion = arguments["CMSSWVersion"]
        self.procScenario = arguments['ProcScenario']
        self.outputs = arguments['Outputs']

        # crashes if this isn't set
        self.globalTag = "NOTSET"

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

def repackWorkload(workloadName, arguments):
    """
    _repackWorkload_

    Instantiate the RepackWorkflowFactory and have
    it generate a workload for the given parameters.
    """
    myRepackFactory = RepackWorkloadFactory()
    return myRepackFactory(workloadName, arguments)
