from T0Component.Tier0Feeder.MultipleAgents.BaseAgent import BaseAgent

class HelperAgent(BaseAgent):
    """
    Helper agent. The streams processed by this one are explicitely defined in the tier0Config. 
    helperRole has to match

    Use it with
    config.Tier0Feeder.AgentRole = "SecondAgent" (or "ThirdAgent" ..., follow the configuration file)
    """
    def __init__(self, tier0Config, helperRole = None):
        BaseAgent.__init__(self, tier0Config)
        self.role = helperRole

        if self.role and self.role in self.MultipleAgentStreams:
            self.streams = self.MultipleAgentStreams[self.role]
        else:
            self.streams = []
        
    def filterStreamerFiles (self, streamerFiles = []):
        """
        _filterStreamerFiles_

        When running multiple agents, filter out data from Storage Manager to avoid duplicates 
        Returns streamers the agent wants to process
        """

        filteredStreamers = [streamer for streamer in streamerFiles if streamerFiles['stream'] in self.streams]

        return filteredStreamers

    def filterHltConfigStreams (self, hltConfig = {}):
        """
        _filterHltConfigStreams_

        When running multiple agents, populate databases with the streams information relevant to the given agent
        Returns modified hltConfig with streams that the agent wants
        """

        filteredHltConfig = {stream: hltConfig['mapping'][stream] for stream in hltConfig['mapping'] if stream in self.streams}

        return filteredHltConfig