######################################
# Google Text to Speech
######################################
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.text_to_speech.tts_abstract import TTS as TTS_Abstract
from gtts import gTTS
# TODO: Replace playsound with audio_player
from os import remove, path
from playsound import playsound


class TTS(TTS_Abstract):
    # The id of the object as it will appear in the json
    id = "Google_TTS"

    def __init__(self, settings_tool: SettingsTool, channels: Channels):
        self.settings_tool = settings_tool
        self.channels = channels
        pass

    def say(self, text):
        # send audio to google and save it as a file
        filename = "tts.mp3"
        google_audio = gTTS(text)
        google_audio.save(filename)

        # play speech then remove the file
        playsound(path.abspath(filename).replace("\\", "/"))
        remove(filename)
