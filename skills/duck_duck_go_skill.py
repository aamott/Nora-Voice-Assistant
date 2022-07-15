####################################
# DuckDuckGo Skill
# Answers queries from the DuckDuckGo API.
####################################
from skills import base_skill
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.audio_utils import AudioUtils
import requests


class Skill(base_skill.BaseSkill):
    name = "DuckDuckGo Skill"

    def __init__(self, settings_tool: SettingsTool, channels: Channels, audio_utils: AudioUtils):
        self.settings_tool = settings_tool
        self.channels = channels
        self.audio_utils = audio_utils


    def intent_creator(self, register_intent: callable):
        """ This function registers intents using register_intent.
            Parameters: 
                register_intent (callable): a function that can add an intent to Nora. """

        # register the duckduckgo intent
        register_intent(
            intent_callback=self.duckduckgo_intent,
            intent_phrases=["Ask duckduckgo (for | ) {query}", "Ask the duck (for | ) {query}"],
            intent_name="duckduckgo")

    def duckduckgo_intent(self, intent_data):
        """ Processes a user's query and speaks the answer from duckduckgo. """
        # get the name entity from the intent.
        query = intent_data["entities"].get("query") + '?'

        # get the answer from duckduckgo.
        response = requests.get("https://api.duckduckgo.com",
                                params={
                                    "q": query,
                                    "format": "json"
                                })
        search_data = response.json()
        answer = search_data.get("Abstract")

        # speak the answer.
        if answer:
            # if the answer is longer than 500 characters, only use the first 3 sentences.
            if len(answer) > 500:
                mini_answer = answer.split(".") 
                mini_answer = mini_answer[:3]
                mini_answer = ".".join(mini_answer)
                self.audio_utils.say(mini_answer)

                usr_input = self.audio_utils.input("Would you like to hear the rest?")
                if 'yes' in usr_input or 'yeah' in usr_input or 'sure' in usr_input:
                    self.audio_utils.say(answer[len(mini_answer):])
        
            else:
                self.audio_utils.say(answer)
        else:
            self.audio_utils.say("DuckDuckGo couldn't find an instant answer for, " + query)

        # return the answer.
        return answer