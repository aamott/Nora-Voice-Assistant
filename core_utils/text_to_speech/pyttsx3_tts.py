######################################
# pyttsx3 Text to Speech
# voices can be set to:
# Microsoft David Desktop
# Microsoft Zira Desktop
# Microsoft Mark Desktop
######################################
from os import remove
from time import sleep
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
        self.engine = None

    
    def init_engine(self):
        self.engine = pyttsx3.init()

        # Add any settings that don't exist yet
        self.populate_settings_tool()
        self.settings_tool.save_settings()

        # default voice
        voice_name = self.settings_tool.get_setting("voice_name")
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
        if new_voice:
            self.engine.setProperty('voice', voice.id)
        else:
            print("Voice not found, using default")
            new_voice = voices[0]
            self.settings_tool.set_setting("voice_name", new_voice.name)


    def get_available_voices(self) -> list:
        """ Returns a list of available voices """
        voices = self.engine.getProperty('voices')
        return [voice for voice in voices]


    def say(self, text):
        """  Play the text as speech
            Args:
                text (str): the text to be spoken
        """
        # for this to work in a thread, we have to 
        # re-initialize the engine every single time.
        # Lag is still small
        self.init_engine()

        try:
            self.engine.save_to_file(text, "tts.wav")
            self.engine.runAndWait()
            sleep(0.05)
            self.audio_player.play_sound("tts.wav")
            remove("tts.wav")
        except Exception as e:
            print("pyttsx3: ", e)

        # free the resources
        self.engine = None


    def populate_settings_tool(self):
        """ Populates the settings tool with the settings for this TTS object """
        self.settings_tool.create_setting("voice_name", 
                                        default_value="Microsoft Zira Desktop - English (United States)")

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
