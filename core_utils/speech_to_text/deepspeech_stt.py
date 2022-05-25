#######################################
# Mozilla DeepSpeech
# Requires:
#     pip install deepspeech-gpu deepspeech
#     pip install -U TTS
#######################################
from core_utils.speech_to_text.stt_abstract import STT as STT_Abstract
from core_utils.core_core.audio_recorder import AudioRecorder
from deepspeech import Model

import numpy as np

class STT( STT_Abstract ):
    # The id of the object as it will appear in the json
    name = "DeepSpeech_STT"
    model_file = 'core_utils/speech_to_text/deepSpeech/deepspeech-0.9.3-models.pbmm'

    def __init__(self, model_file=model_file):
        self.audio_recorder = AudioRecorder(samplerate=16000)

        self.ds = Model(model_file)
        # print("Samplerate of Deepspeech Model: ", self.ds.sampleRate())


    def calibrate_audio(self):
        """
        Calibrates the audio recorder
        """
        self.audio_recorder.calibrate_silence()


    def listen(self):
        # Get audio BytesIO object
        audio = self.audio_recorder.get_recording()

        # get text with DeepSpeech (ds)
        return self.ds.stt(audio)


if __name__ == "__main__":
    stt = STT()
    print("Listening...")
    print(stt.listen())
