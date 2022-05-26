######################################
# pyttsx3 Text to Speech
######################################
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.text_to_speech.tts_abstract import TTS as TTS_Abstract
import pyttsx3

class TTS(TTS_Abstract):
    # The id of the object as it will appear in the json
    id = "pyttsx3_TTS"

    def __init__(self, settings_tool: SettingsTool, channels: Channels):
        self.settings_tool = settings_tool
        self.channels = channels
        
        self.engine = pyttsx3.init()

        # default voice
        voices = self.get_available_voices()
        self.set_voice(voices[1])


    def set_voice(self, voice="en-US_AllisonVoice"):
        self.engine.setProperty('voice', voice)


    def get_available_voices(self):
        voices = self.engine.getProperty('voices')
        return [voice.id for voice in voices]


    def say(self, text):
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



if __name__ == "__main__":
    tts = TTS()
    tts.say("Hello World")