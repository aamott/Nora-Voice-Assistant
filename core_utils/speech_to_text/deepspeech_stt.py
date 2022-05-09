#######################################
# Mozilla DeepSpeech
# Requires:
#     /python39.scripts/pip3.9.exe install deepspeech-gpu deepspeech
#     pip install -U TTS
#######################################
from deepspeech import Model
# For listening to mic
import io
import soundfile as sf


class STT:
    # The id of the object as it will appear in the json
    name = "DeepSpeech_STT"

    def __init__(self, model_file='deepSpeech/deepspeech-0.9.3-models.pbmm'):
        # Initialize stuff for recording with SpeechRecognition package
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()
        with self.mic as source:
            self.r.adjust_for_ambient_noise(source)

        self.ds = Model(model_file)

    def record_mic(self, samplerate=16000):
        """Records audio, stopping at first silence
            
            Records audio using the SpeechRecognition library
            then converts it to a wav file in Numpy array form
            for DeepSpeech.
            For information on the SpeechRecognition AudioData object, visit
            https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst

            Args:
                int samplerate  --  Samplerate the file should be returned with. 
            Returns:
                int samplerate  -- Must match the samplerate of the model trained!
                numpy.int16[] data -- wav audio file as an int16 Numpy array
        """
        # record
        print("Listening...")
        with self.mic as source:
            audioData = self.r.listen(source)
        print("Done listening")

        # convert to an int16 numpy array for DeepSpeech
        raw_wav = audioData.get_wav_data(convert_rate=samplerate)
        data, samplerate = sf.read(io.BytesIO(raw_wav), dtype="int16")
        return samplerate, data

    def listen(self):
        samplerate, data = self.record_mic()
        # get text with DeepSpeech (ds)
        return self.ds.stt(data)
