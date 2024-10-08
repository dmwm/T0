import logging
from T0Component.Tier0Feeder.MultipleAgents.BaseAgent import BaseAgent

class MainAgent(BaseAgent):
    """
    Main agent. The streams processed by this agent are implicitely defined in the tier0Config
    * This agent will process streams that are not defined in any of the other agents
    * tier0Config.Global.HelperAgentStreams = {'SecondAgent' : ["stream_1", "stream_2"],
                                                 'ThirdAgent' : ["stream_3", "stream_4"]}
    Note: This agent will ignore all streams in the helper agents, regardless of the helper agents status
    """
    def __init__(self, tier0Config):
        
        BaseAgent.__init__(self, tier0Config)
        self.name = "MainAgent"
        self.findUnwantedStreams()
        logging.info("This is a MainAgent. Ignoring streams {}".format(self.rejectStreams))
        
    def filterStreamerFiles (self, streamerFiles):
        """
        _filterStreamerFiles_

        When running multiple agents, filter out data from Storage Manager to avoid duplicates 
        Returns the streamers the agent want to process
        """
        filteredStreamers = [streamer for streamer in streamerFiles if streamer['stream'] not in self.rejectStreams]

        return filteredStreamers

    def filterHltConfigStreams (self, hltStreamMapping = {}):
        """
        _filterHltConfigStreams_

        When running multiple agents, populate databases with the streams information relevant to the given agent
        """
        filteredHltStreamMapping = {stream: hltStreamMapping[stream] for stream in hltStreamMapping if stream not in self.rejectStreams}

        return filteredHltStreamMapping

    def findUnwantedStreams (self):
        """
        _findUnwantedStreams_

        Returns a list of streams that will not be processed by any other agent
        """
        self.rejectStreams = []
        for agent in self.helperAgentStreams.keys():
            self.rejectStreams += self.helperAgentStreams[agent]
        
        return