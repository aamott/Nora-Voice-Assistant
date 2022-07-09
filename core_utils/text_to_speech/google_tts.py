######################################
# Google Text to Speech
######################################
from core_utils.core_core.audio_player import AudioPlayer
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.text_to_speech.tts_abstract import TTS as TTS_Abstract
from gtts import gTTS
from os import remove
from pydub import AudioSegment


class TTS(TTS_Abstract):
    # The id of the object as it will appear in the json
    name = "Google_TTS"

    def __init__(self, settings_tool: SettingsTool, channels: Channels, audio_player: AudioPlayer):
        self.settings_tool = settings_tool
        self.channels = channels
        self.audio_player = audio_player


    def say(self, text):
        """ Speaks the text. """
        # TODO: Write to a file-like object instead of a file
        # send audio to google and save it as a file
        filename = "tts"
        google_audio = gTTS(text)
        google_audio.save(filename)

        # convert the file to a wav
        audio_file = AudioSegment.from_mp3(filename)
        audio_file.export(filename, format="wav")
        
        # play speech
        self.audio_player.play_sound(filename)

        # remove the mp3 and wav files
        remove(filename)


    def populate_settings_tool(self):
        """ Populates the settings tool with the settings for this TTS object """
        # self.settings_tool.set_setting("language", None)
        pass
