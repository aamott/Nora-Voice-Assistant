#######################
# Hello World Skill
#######################
from skills import base_skill
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.audio_utils import AudioUtils

class Skill(base_skill.BaseSkill):
    name = "Hello World Skill"


    def __init__(self, settings_tool: SettingsTool, channels: Channels, audio_utils: AudioUtils):
        self.settings_tool = settings_tool
        self.channels = channels
        self.audio_utils = audio_utils


    def intent_creator(self, register_intent: callable):
        """ registers intents using register_intent """
        # Register the hello_world_intent function. 
        # This will be called whenever intent_phrases are detected.
        intent_phrases = ["hello (world | )"] # this translates to "hello world" or "hello"
        register_intent(intent_callback=self.hello_world_intent,
                        intent_phrases=intent_phrases,
                        intent_name="say_hello")


    def hello_world_intent(self, intent_data):
        """ hello world intent 
            This function is called when the intent is detected.
            Parameters:
                intent_data (dict): the intent data
        """
        self.audio_utils.say("Hello World!")

        # Some skills may want to implement sassiness or other personality traits. 
        # Every intent has a "sassiness" attribute that is automatically generated
        # by the intent parser. Its value is a number between 0 and 10.
        if intent_data.get("sassiness") > 3:
            self.audio_utils.say("I'm sassy!")
