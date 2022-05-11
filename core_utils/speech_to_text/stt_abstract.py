#######################################
# Abstract for STT classes
# All STT classes must inherit from this class
#######################################
from abc import ABC, abstractmethod
from core_utils.core_core.audio_recorder import AudioRecorder

class STT(ABC):
    # The id of the object as it will appear in the json
    name = "Abstract_STT" # Replace this with the actual implementation

    def __init__(self):
        self.audio_recorder = AudioRecorder()

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