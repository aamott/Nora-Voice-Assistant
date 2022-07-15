############################
# Wolfram Alpha Skill
############################
from skills import base_skill
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.audio_utils import AudioUtils
import wolframalpha


class Skill(base_skill.BaseSkill):
    name = "Wolfram Alpha Skill"

    def __init__(self, settings_tool: SettingsTool, channels: Channels, audio_utils: AudioUtils):
        self.settings_tool = settings_tool
        self.channels = channels
        self.audio_utils = audio_utils

        self.settings_tool.create_setting("wolfram_alpha_app_id")
        app_id = self.settings_tool.get_setting("wolfram_alpha_app_id")
        if app_id is None:
            # throw an exception to stop the skill from loading.
            raise Exception("Wolfram alpha app id not set.")

        self.client = wolframalpha.Client(app_id)

    def intent_creator(self, register_intent: callable):
        """ This function registers intents using register_intent.
            Parameters: 
                register_intent (callable): a function that can add an intent to Nora. """

        # register the wolfram alpha intent
        register_intent(
            intent_callback=self.wolfram_alpha_intent,
            intent_phrases=["Ask wolfram (alpha | ) {search_phrase}"],
            intent_name="wolfram_alpha")

    def wolfram_alpha_intent(self, intent_data):
        """ Processes a user's query and speaks the answer from wolfram alpha. """
        # get the name entity from the intent.
        search_phrase = intent_data["entities"].get("search_phrase")

        # get the answer from wolfram alpha.
        response = self.client.query(search_phrase)
        answer = next(response.results).text

        # speak the answer.
        self.audio_utils.say(answer)

        # return the answer.
        return answer