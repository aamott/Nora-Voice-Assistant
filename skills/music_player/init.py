###########################
# Music Player Skill
###########################
from skills import base_skill
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool


class Skill(base_skill.Skill):
    name = "Music Player"

    def __init__(self, settings_tool: SettingsTool, channels: Channels) -> None:
        self.settings_tool = settings_tool
        self.channels = channels


    def intent_creator(self, register_intent: callable):
        """ registers intents using register_intent
        """
        # TODO: register intents
        pass