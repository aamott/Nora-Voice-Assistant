#######################################
# Stub Speech to Text
#  Acts as a stand-in for the real STT module
#######################################
from core_utils.speech_to_text.stt_abstract import STT as STT_Abstract

class STT( STT_Abstract ):
    # The id of the object as it will appear in the json
    name = "Stub_STT"

    def __init__(self):
        # Initialize stuff for speech recognition
        pass

    def calibrate_audio(self):
        pass

    def listen(self):
        text = "Hello, world!"
        return text
