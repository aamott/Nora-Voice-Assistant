#######################################
# Abstract for STT classes
# All STT classes must inherit from this class
#######################################
from abc import ABC, abstractmethod
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.core_core.audio_recorder import AudioRecorder

class STT(ABC):
    # The id of the object as it will appear in the json
    name = "Abstract_STT" # Replace this with the actual implementation

    @abstractmethod
    def __init__(self, settings_tool: SettingsTool, channels: Channels,
                 audio_recorder: AudioRecorder):
        self.settings_tool = settings_tool
        self.channels = channels
        self.audio_recorder = audio_recorder

    @abstractmethod
    def calibrate_audio(self):
        """ This method calibrates the audio recorder.
            Probably:
            self.audio_recorder.calibrate_silence()
        """
        self.audio_recorder.calibrate_silence()

    @abstractmethod
    def listen(self) -> str:
        """ Listens for audio, then returns the text of the audio 

        Returns:
            str -- The text of the audio
        """
        pass