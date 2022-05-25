#######################################
# Stub Speech to Text
#  Acts as a stand-in for the real STT module
#######################################
from core_utils.speech_to_text.stt_abstract import STT as STT_Abstract
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.core_core.audio_recorder import AudioRecorder

class STT( STT_Abstract ):
    # The id of the object as it will appear in the json
    name = "Stub_STT"

    def __init__(self, settings_tool: SettingsTool, channels: Channels,
                 audio_recorder: AudioRecorder):
        # Initialize stuff for speech recognition
        pass

    def calibrate_audio(self):
        pass

    def listen(self):
        text = "hello world"
        return text
