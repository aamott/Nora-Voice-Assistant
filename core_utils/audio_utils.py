#################################
# Audio Utilities
# Allows easy access to audio recording, playback, and user voice input
# through Audio_Recorder and Audio_Player
#################################
from numpy import ndarray
# from core_utils.core_core.audio_player import AudioPlayer
from core_utils.core_core.audio_recorder import AudioRecorder
from core_utils.settings_tool import SettingsTool
import core_utils.speech_to_text_getter as stt_getter
import core_utils.text_to_speech_getter as tts_getter


class AudioUtils:

    def __init__(self, settings_tool: SettingsTool):
        self.settings_tool=settings_tool
        # Audio Setup
        # self._audio_player = AudioPlayer()
        self._audio_recorder = AudioRecorder()
        # Speech Setup
        self._stt = stt_getter.get_stt_object(stt_type="stub")
        self._tts = tts_getter.get_tts_object(tts_type="pyttsx3")



    ###########################
    # Speech Interaction
    ###########################
    def listen(self):
        """Listen for user input.

        Returns:
            str: The user's input.
        """
        text = self._stt.listen()
        return text


    def say(self, text):
        """Speak text.

        Args:
            text (str): The text to speak.
        """
        self._tts.say(text)


    ###########################
    # Playback
    ###########################

    def play(self, filename:str = None, audio_data:ndarray = None):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def stop(self):
        pass

    def play_soundeffect(self, filename: str = None, audio_data: ndarray = None):
        pass

    def stop_soundeffects(self):
        pass


    ###########################
    # Recording
    ###########################

    def get_recording(self, samplerate=48000, channels=1, filename=None, max_recording_seconds=8) -> ndarray:
        """Record audio from the microphone for a specified time.
            Args:
                samplerate (int): sample rate of the audio. Defaults to 48000.
                channels (int): number of channels
                filename (str): filename to save the audio to
                max_recording_seconds (int): maximum number of seconds to record

            Returns:
                ndarray [int16]: audio data
        """
        recording = self._audio_recorder.record_audio(samplerate=samplerate,
                                                                        channels=channels,
                                                                        filename=filename,
                                                                        max_recording_seconds=max_recording_seconds)
        return recording


    def calibrate_silence(self) -> int:
        """ Calibrate the silence threshold.

        Returns:
            int: The calibrated silence threshold.
        """
        silence_threshold = self._audio_recorder.calibrate_silence()
        return silence_threshold