#######################################
# Google Cloud Speech-to-Text
#######################################
from core_utils.speech_to_text.stt_abstract import STT as STT_Abstract
from core_utils.core_core.audio_recorder import AudioRecorder
import speech_recognition as sr


class STT( STT_Abstract ):
    # The id of the object as it will appear in the json
    name = "Google_STT"

    def __init__(self, credentials_file='credentials.json'):
        self.audio_recorder = AudioRecorder()
        self.recognizer = sr.Recognizer()


    def calibrate_audio(self):
        """
        Calibrates the audio recorder
        """
        self.audio_recorder.calibrate_silence()


    def listen(self):
        """
        Listens for audio, then returns the text of the audio
        """
        # record
        audio_file = self.audio_recorder.get_recording_as_wav()

        # convert to AudioData object
        # Obtained from https://stackoverflow.com/questions/61961587/can-i-do-recognition-from-numpy-array-in-python-speechrecognition
        audio_data = sr.AudioData(audio_file.read(), 48000, 2)

        # recognize
        try:
            text = self.recognizer.recognize_google(audio_data)
            print("Done listening")
            return text

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return None

        # with self.mic as source:
        #     audioData = self.sr.listen(source)
