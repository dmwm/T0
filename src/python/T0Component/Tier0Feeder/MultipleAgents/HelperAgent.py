import logging
from T0Component.Tier0Feeder.MultipleAgents.BaseAgent import BaseAgent

class HelperAgent(BaseAgent):
    """
    Helper agent. The streams processed by this one are explicitely defined in the tier0Config. 
    helperRole has to match

    Use it with
    config.Tier0Feeder.AgentRole = "SecondAgent" (or "ThirdAgent" ..., follow the configuration file)
    Note: if the helperName is none or unknown, returned values will be empty and no data is injected
    """
    def __init__(self, tier0Config, helperName = None):
        
        BaseAgent.__init__(self, tier0Config)
        self.name = helperName
        if self.name and self.name in self.helperAgentStreams:
            self.streams = self.helperAgentStreams[self.name]
        else:
            self.streams = []
        
        logging.info("This is a HelperAgent named {}. Processing streams {}".format(self.name, self.streams))

    def filterStreamerFiles (self, streamerFiles = []):
        """
        _filterStreamerFiles_

        When running multiple agents, filter out data from Storage Manager to avoid duplicates 
        Returns streamers the agent wants to process
        """

        filteredStreamers = [streamer for streamer in streamerFiles if streamer['stream'] in self.streams]

        return filteredStreamers

    def filterHltConfigStreams (self, hltStreamMapping = {}):
        """
        _filterHltConfigStreams_

        When running multiple agents, populate databases with the streams information relevant to the given agent
        Returns modified hltStreamMapping with streams that the agent wants
        """

        filteredHltStreamMapping = {stream: hltStreamMapping[stream] for stream in hltStreamMapping if stream in self.streams}

        return filteredHltStreamMapping