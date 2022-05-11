######################################
# Command Line TTS
# Prints text to the command line instead of speaking it
######################################
from core_utils.text_to_speech.tts_abstract import TTS as TTS_Abstract

class TTS(TTS_Abstract):
    # The id of the object as it will appear in the json
    id = "Command Line TTS"

    def __init__(self):
        pass

    def say(self, text):
        # send audio to google and save it as a file
        print(text)
