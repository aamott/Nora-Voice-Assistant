###################################
# System Manager Skill
# This skill is used to manage the system, such as
# restarting the system, or shutting down the system.
###################################
from skills import base_skill
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.audio_utils import AudioUtils


class Skill(base_skill.BaseSkill):
    name = "System Manager Skill"

    def __init__(self, settings_tool: SettingsTool, channels: Channels,
                 audio_utils: AudioUtils):
        self.settings_tool = settings_tool
        self.channels = channels
        self.audio_utils = audio_utils


    def intent_creator(self, register_intent: callable):
        """ This function registers intents using register_intent.
            Parameters: 
                register_intent (callable): a function that can register an intent 
        """
        register_intent(intent_callback=self.shutdown_intent,
                        intent_phrases=["Shut(| )down the system"],
                        intent_name="shutdown_intent")


    def shutdown_intent(self, intent_data):
        """This is the function that is called when the intent is detected."""
        self.audio_utils.say("Shutting down...")
        self.channels.publish("shutdown", 'system')
