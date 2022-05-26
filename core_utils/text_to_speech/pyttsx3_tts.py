######################################
# pyttsx3 Text to Speech
######################################
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.text_to_speech.tts_abstract import TTS as TTS_Abstract
import pyttsx3

class TTS(TTS_Abstract):
    # The id of the object as it will appear in the json
    name = "pyttsx3_TTS"

    def __init__(self, settings_tool: SettingsTool, channels: Channels):
        self.settings_tool = settings_tool
        self.channels = channels

        # Add any settings that don't exist yet
        self.populate_settings_tool()
        self.settings_tool.save_settings()

        self.engine = pyttsx3.init()

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
        if voice is None:
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
        self.engine.say(text)
        self.engine.runAndWait()

        # # Leaving this here for now, for when we come back to threading.
        # # When we threaded before, the code hung with the .say() call, and this fixed it.
        # # Workaround: save to a file and play that.
        # self.engine.save_to_file(text, "temp.mp3")
        # PlaySound("temp.mp3", SND_FILENAME)
        # self.engine.runAndWait()
        # # remove the file
        # os.remove("temp.mp3")


    def populate_settings_tool(self):
        """ Populates the settings tool with the settings for this TTS object """
        if self.settings_tool.get_setting("voice_name") is None:
            self.settings_tool.set_setting("voice_name", "Microsoft Zira Desktop - English (United States)")



if __name__ == "__main__":
    tts = TTS()
    tts.say("Hello World")