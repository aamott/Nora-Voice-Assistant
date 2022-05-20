######################################
# pyttsx3 Text to Speech
######################################
from winsound import SND_FILENAME, PlaySound
import os
from core_utils.text_to_speech.tts_abstract import TTS as TTS_Abstract
import pyttsx3

class TTS(TTS_Abstract):
    # The id of the object as it will appear in the json
    id = "pyttsx3_TTS"

    def __init__(self, ):
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
        # TODO: currently, if we use "say" in different threads, even at different times, it breaks.
        # self.engine.say(text)
        # Workaround: save to a file and play that.
        self.engine.save_to_file(text, "temp.mp3")
        self.engine.runAndWait()
        PlaySound("temp.mp3", SND_FILENAME)

        # remove the file
        os.remove("temp.mp3")



if __name__ == "__main__":
    tts = TTS()
    tts.say("Hello World")