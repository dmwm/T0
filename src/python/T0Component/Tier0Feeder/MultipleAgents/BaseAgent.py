class BaseAgent(object):
    """
    Base agent. 

    """

    def __init__(self, tier0Config):
        
        object.__init__(self)
        self.helperAgentStreams = tier0Config.Global.HelperAgentStreams

    def filterStreamerFiles (self, streamerFiles = []):
        """
        _filterStreamerFiles_

        When running multiple agents, filter out data from Storage Manager to avoid duplicates 
        """
        return 

    def filterHltConfigStreams (self, hltStreamMapping = {}):
        """
        _filterHltConfigStreams_

        When running multiple agents, populate databases with the streams information relevant to the given agent
        """
        return
        