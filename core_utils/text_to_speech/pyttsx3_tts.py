######################################
# pyttsx3 Text to Speech
# voices can be set to:
# Microsoft David Desktop
# Microsoft Zira Desktop
# Microsoft Mark Desktop
######################################
from os import remove
from ..core_core.audio_player import AudioPlayer
from ..core_core.channels import Channels
from ..settings_tool import SettingsTool
from .tts_abstract import TTS as TTS_Abstract
import pyttsx3

class TTS(TTS_Abstract):
    # The id of the object as it will appear in the json
    name = "pyttsx3_TTS"

    def __init__(self, settings_tool: SettingsTool, channels: Channels, audio_player: AudioPlayer):
        self.settings_tool = settings_tool
        self.channels = channels
        self.audio_player = audio_player

        self.engine = pyttsx3.init()

        # Add any settings that don't exist yet
        self.populate_settings_tool()
        self.settings_tool.save_settings()

        # default voice
        voice_name = self.settings_tool.get_setting(
            "voice_name") or "Microsoft Zira Desktop - English (United States)"
        self.set_voice(voice_name)


    def set_voice(self,
                  voice_name="Microsoft Zira Desktop - English (United States)"):
        """ Sets the voice to use for the TTS engine 
            Args:
                voice_name (str): the name of the voice to use
        """
        new_voice = None
        voices = self.get_available_voices()

        # find the voice by name
        for voice in voices:
            if voice.name == voice_name:
                self.settings_tool.set_setting("voice_name", voice_name)
                new_voice = voice
                break

            # if we didn't find the voice, use the default
            print("Voice not found, using default")
            new_voice = voices[0]
            self.settings_tool.set_setting("voice_name", new_voice.name)

        self.engine.setProperty('voice', voice.id)


    def get_available_voices(self) -> list:
        """ Returns a list of available voices """
        voices = self.engine.getProperty('voices')
        return [voice for voice in voices]


    def say(self, text):
        """  Play the text as speech
            Args:
                text (str): the text to be spoken
        """
        # self.engine.say(text)
        # self.engine.runAndWait()

        # save the speech to a file buffer

        self.engine.save_to_file(text, "tts.wav")
        self.engine.runAndWait()
        self.audio_player.play_sound("tts.wav")
        # remove the file
        remove("tts.wav")


    def populate_settings_tool(self):
        """ Populates the settings tool with the settings for this TTS object """
        if self.settings_tool.get_setting("voice_name") is None:
            self.settings_tool.set_setting("voice_name", "Microsoft Zira Desktop - English (United States)")

        # show a list of voices
        voices = self.get_available_voices()
        voice_names = [voice.name for voice in voices]
        self.settings_tool.set_setting("voice_name (options)", voice_names)



if __name__ == "__main__":
    tts = TTS()
    tts.say("Hello World")

    # print available voices
    voices = tts.get_available_voices()
    for voice in voices:
        print(voice.name)
    print("")
