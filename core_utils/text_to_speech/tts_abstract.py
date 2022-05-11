#######################################
# Abstract for TTS classes
# All TTS classes must inherit from this class
#######################################
from abc import ABC, abstractmethod

class TTS(ABC):
    # The id of the object as it will appear in the json
    name = "Abstract_TTS" # Replace this with the actual implementation

    def __init__(self):
        pass


    @abstractmethod
    def say(self, text: str):
        """  Play the text as speech 
            Args:
                text (str): the text to be spoken
        """
        pass