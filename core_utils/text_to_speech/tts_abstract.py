#######################################
# Abstract for TTS classes
# All TTS classes must inherit from this class
#######################################
from abc import ABC, abstractmethod
from core_utils.core_core.audio_player import AudioPlayer
from core_utils.core_core.channels import Channels
from ..settings_tool import SettingsTool

class TTS(ABC):
    # The id of the object as it will appear in the json
    name = "Abstract_TTS" # Replace this with the actual implementation

    @abstractmethod
    def __init__(self, settings_tool: SettingsTool, channels: Channels, audio_player: AudioPlayer):
        pass


    @abstractmethod
    def say(self, text: str):
        """  Play the text as speech 
            Args:
                text (str): the text to be spoken
        """
        pass


    @abstractmethod
    def populate_settings_tool(self):
        """ Populates the settings tool with the settings for this STT object
        """
        pass