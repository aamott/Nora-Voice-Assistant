#########################
# Base Skill Class
#########################
from abc import ABC, abstractmethod
from core_utils.settings_tool import SettingsTool

class Skill(ABC):

    def __init__(self, settings_tool: SettingsTool=None) -> None:
        """ Initialize the Skill

        """
        pass


    @abstractmethod
    def intent_creator(self, register_intent: callable):
        """ registers intents using register_intent
        """
        pass