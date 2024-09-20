from T0Component.Tier0Feeder.MultipleAgents.BaseAgent import BaseAgent

class MainAgent(BaseAgent):
    """
    Main agent. The streams processed by this agent are implicitely defined in the tier0Config
    * This agent will process streams that are not defined in any of the other agents
    * tier0Config.Global.MultipleAgentStreams = {'SecondAgent' : ["stream_1", "stream_2"],
                                                 'ThirdAgent' : ["stream_3", "stream_4"]}

    """
    def __init__(self, tier0Config):
        BaseAgent.__init__(self, tier0Config)
        self.rejectStreams = self.findUnwantedStreams()
        
    def filterStreamerFiles (self, streamerFiles):
        """
        _filterStreamerFiles_

        When running multiple agents, filter out data from Storage Manager to avoid duplicates 
        Returns the streamers the agent want to process
        """
        filteredStreamers = [streamer for streamer in streamerFiles if streamerFiles['stream'] not in self.rejectStreams]

        return filteredStreamers

    def filterHltConfigStreams (self, hltConfig):
        """
        _filterHltConfigStreams_

        When running multiple agents, populate databases with the streams information relevant to the given agent
        """
        filteredHltConfig = {stream: hltConfig['mapping'][stream] for stream in hltConfig['mapping'] if stream not in self.rejectStreams}

        return

    def findUnwantedStreams (self):
        """
        _findUnwantedStreams_

        Returns a list of streams that will not be processed by any other agent
        """
        self.rejectStreams = []
        for agent in self.multipleAgentStreams.keys():
            self.rejectStreams += self.multipleAgentStreams[agent]
        
        return