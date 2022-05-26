#########################
# Base Skill Class
# The Base Class for all Skills
#########################
from abc import ABC, abstractmethod
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.audio_utils import AudioUtils

class BaseSkill(ABC):
    @abstractmethod
    def __init__(self, settings_tool: SettingsTool, channels: Channels, audio_utils: AudioUtils):
        """ Initialize the Skill

        """
        pass


    @abstractmethod
    def intent_creator(self, register_intent: callable):
        """ registers intents using register_intent
        """
        pass