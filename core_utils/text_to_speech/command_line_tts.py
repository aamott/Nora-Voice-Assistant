######################################
# Command Line TTS
# Prints text to the command line instead of speaking it
######################################
from core_utils.core_core.audio_player import AudioPlayer
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.text_to_speech.tts_abstract import TTS as TTS_Abstract

class TTS(TTS_Abstract):
    # The id of the object as it will appear in the json
    name = "Print"

    def __init__(self, settings_tool: SettingsTool, channels: Channels, audio_player: AudioPlayer):
        self.settings_tool = settings_tool
        self.channels = channels
        pass

    def say(self, text):
        # send audio to google and save it as a file
        print(text)

    def populate_settings_tool(self):
        """ Populates the settings tool with the settings for this TTS object """
        # self.settings_tool.set_setting("key", None)
        pass