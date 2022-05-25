#######################################
# Mozilla DeepSpeech
# Requires:
#     pip install deepspeech-gpu deepspeech
#     pip install -U TTS
#######################################
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.speech_to_text.stt_abstract import STT as STT_Abstract
from core_utils.core_core.audio_recorder import AudioRecorder
from deepspeech import Model

import numpy as np

class STT( STT_Abstract ):
    # The id of the object as it will appear in the json
    name = "DeepSpeech_STT"
    model_file = 'core_utils/speech_to_text/deepSpeech/deepspeech-0.9.3-models.pbmm'

    def __init__(self, settings_tool: SettingsTool, channels: Channels,
                 audio_recorder: AudioRecorder, model_file: str = model_file):
        self.settings_tool = settings_tool
        self.channels = channels
        self.audio_recorder = audio_recorder or AudioRecorder()

        self.ds = Model(model_file)
        # print("Samplerate of Deepspeech Model: ", self.ds.sampleRate())


    def calibrate_audio(self):
        """
        Calibrates the audio recorder
        """
        self.audio_recorder.calibrate_silence()


    def listen(self):
        # Get audio BytesIO object
        audio = self.audio_recorder.get_recording(samplerate=16000)

        # get text with DeepSpeech (ds)
        return self.ds.stt(audio)


if __name__ == "__main__":
    stt = STT()
    print("Listening...")
    print(stt.listen())
