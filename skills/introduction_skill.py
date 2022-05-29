###########################
# Introduction Skill
###########################
from skills import base_skill
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.audio_utils import AudioUtils


class Skill(base_skill.BaseSkill):
    name = "Introduction Skill"
    introduction = "Hello, I am Nora. I am your virtual assistant."


    def __init__(self, settings_tool: SettingsTool, channels: Channels, audio_utils: AudioUtils):
        self.settings_tool = settings_tool
        self.channels = channels
        self.audio_utils = audio_utils


    def intent_creator(self, register_intent: callable):
        """ registers intents using register_intent """
        register_intent(intent_callback=self.introduction_intent,
                        intent_phrases=["introduce yourself"],
                        intent_name="say_introduce")


    def introduction_intent(self, intent_data):
        introduction = self.settings_tool.get_setting("introduction")
        self.audio_utils.say(introduction)


    def populate_settings(self):
        if not self.settings_tool.setting_exists("introduction"):
            self.settings_tool.set_setting(self.introduction)