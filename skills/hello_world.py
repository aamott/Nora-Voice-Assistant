#######################
# Hello World Skill
#######################
from skills import base_skill
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.audio_utils import AudioUtils

class Skill(base_skill.Skill):
    name = "Hello World Skill"


    def __init__(self, settings_tool: SettingsTool, channels: Channels, audio_utils: AudioUtils):
        self.settings_tool = settings_tool
        self.channels = channels
        self.audio_utils = audio_utils


    def intent_creator(self, register_intent: callable):
        """ registers intents using register_intent """
        register_intent(intent_callback=self.hello_world_intent,
                        intent_phrases=["hello (world | )"],
                        intent_name="say_hello")


    def hello_world_intent(self, intent_data):
        print("Hello World!")
        self.audio_utils.say("Hello World!")
