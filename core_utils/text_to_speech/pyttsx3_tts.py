######################################
# pyttsx3 Text to Speech
######################################
from core_utils.text_to_speech.tts_abstract import TTS as TTS_Abstract
import pyttsx3

class TTS(TTS_Abstract):
    # The id of the object as it will appear in the json
    id = "pyttsx3_TTS"

    def __init__(self, ):
        self.engine = pyttsx3.init()


    def set_voice(self, voice="en-US_AllisonVoice"):
        self.engine.setProperty('voice', voice)


    def get_available_voices(self):
        voices = self.engine.getProperty('voices')
        return [voice.id for voice in voices]


    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()



if __name__ == "__main__":
    tts = TTS()
    tts.say("Hello World")