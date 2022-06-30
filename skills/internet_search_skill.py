#######################
# Hello World Skill
#######################
from skills import base_skill
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.audio_utils import AudioUtils
import webbrowser

class Skill(base_skill.BaseSkill):
    name = "Internet Search Skill"

    def __init__(self, settings_tool: SettingsTool, channels: Channels, audio_utils: AudioUtils):
        self.settings_tool = settings_tool
        self.channels = channels
        self.audio_utils = audio_utils


    def intent_creator(self, register_intent: callable):
        """ This function registers intents using register_intent.
            Parameters: 
                register_intent (callable): a function that can add an intent to Nora. """

        # register the internet search intent
        register_intent(
            intent_callback=self.internet_search_intent,
            # We can add 'entities', (or named values to look for), to the intent.
            intent_phrases=[
                "Search (for | ) {search_phrase}", "Look up {search_phrase}"
            ],
            intent_name="Internet_search")


    def internet_search_intent(self, intent_data):
        """This is a slightly fancier version of the hello world intent.
                It takes a name as a parameter and says hello to that name."""
        # get the name entity from the intent.
        search_phrase = intent_data["entities"].get("search_phrase")

        self.audio_utils.say("Searching")

        url = f"https://www.google.com/search?q={search_phrase}"

        webbrowser.open(url)
