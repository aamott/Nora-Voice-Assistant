#################################
# Audio Utilities
# Allows easy access to audio recording, playback, and user voice input
# through Audio_Recorder and Audio_Player
#################################
from numpy import ndarray
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.core_core.audio_recorder import AudioRecorder
import core_utils.speech_to_text_getter as stt_getter
import core_utils.text_to_speech_getter as tts_getter
from core_utils.core_core.audio_player import AudioPlayer


class AudioUtils:

    def __init__(self, channels: Channels,
                 settings_tool: SettingsTool,
                 stt_type: str = "Google_STT",
                 tts_module: str = "pyttsx3_TTS"):
        self.settings_tool=settings_tool
        # Audio Setup
        self._audio_player = AudioPlayer()
        recorder_settings = self.settings_tool.get_sub_tool("audio_recorder")
        self._audio_recorder = AudioRecorder(settings_tool=recorder_settings)

        # Speech to Text Setup
        stt_settings_tool = settings_tool.get_sub_tool("speech_to_text")
        self._stt = stt_getter.get_stt_object(
            stt_module=stt_type,
            channels=channels,
            settings_tool=stt_settings_tool,
            audio_recorder=self._audio_recorder)
        # Text to Speech Setup
        tts_settings_tool = settings_tool.get_sub_tool("text_to_speech")
        self._tts = tts_getter.get_tts_object(
            tts_module=tts_module,
            channels=channels,
            settings_tool=tts_settings_tool,
            audio_player=self._audio_player)



    ###########################
    # Speech Interaction
    ###########################
    def input(self, prompt: str) -> str:
        """Prompt the user for input.

        Args:
            prompt (str): The prompt to say to the user.

        Returns:
            str: The user's input.
        """
        self.say(prompt)
        text = self.listen()
        return text


    def listen(self):
        """Listen for user input.

        Returns:
            str: The user's input.
        """
        text = self._stt.listen()
        return text


    def say(self, text: str):
        """Speak text.

        Args:
            text (str): The text to speak.
        """
        # throw an error if the text is empty
        if text == "" or text == None:
            raise ValueError("Text to speak is empty.")
        print("+ ", text)
        try:
            self._tts.say(text)
        except Exception as e:
            print("Exception in audio_utils->say: ", e)


    ###########################
    # Playback
    ###########################

    def play(self, filename:str = None):
        self._audio_player.play(filename)


    def pause(self):
        self._audio_player.pause()


    def resume(self):
        self._audio_player.resume()


    def stop(self):
        self._audio_player.stop()


    def play_sound(self, filename: str = None):
        pass


    def stop_sound(self):
        self._audio_player.stop_sound()
    
    def get_volume(self):
        self._audio_player.get_volume()
    
    def decrease_volume(self):
        self._audio_player.descrease_volume()
    
    def increase_volume(self):
        self._audio_player.increase_volume()
    
    def min_volume(self):
        self._audio_player.set_min_volume()
    
    def max_volume(self):
        self._audio_player.set_max_volume()


    ###########################
    # Recording
    ###########################

    def get_recording(self, samplerate=48000, channels=1, filename=None, max_recording_seconds=8) -> ndarray:
        """Record audio from the microphone for a specified time or until silence is detected.
            Args:
                samplerate (int): sample rate of the audio. Defaults to 48000.
                channels (int): number of channels
                filename (str): filename to save the audio to
                max_recording_seconds (int): maximum number of seconds to record

            Returns:
                ndarray [int16]: audio data
        """
        recording = self._audio_recorder.record_until_silence(
            samplerate=samplerate,
            channels=channels,
            filename=filename,
            max_recording_seconds=max_recording_seconds)
        return recording


    # def record_continuous_using_callback(self,
    #                       frame_processor_callback: callable,
    #                       frame_length=1248,
    #                       samplerate=16000,
    #                       channels=1,
    #                       timeout=None):
    #     """ Record audio from the microphone in a continuous loop.
    #         Args:
    #             frame_processor_callback (callable->bool): function to pass audio frames to.
    #                                 Should accept numpy array of audio data, which is split into channels, and return True if recording should continue. Audio data is split into frames of length frame_length.
    #                                 A frame is a single point of audio data, represented by an number. Each frame has channels, usually 1 or 2.
    #                                 audio data is an array of frames.
    #                                 audio data can be visualized as follows:
    #                                     audio_data = [frame1, frame2, frame3, ...]
    #                                     frame1 = [channel1_data, channel2_data, ...]
    #                                     channel1_data = 60
    #                                 15       .                          .''.
    #                                 10     .' .                       .'    '..     .
    #                                 5    ..'    '.                 .'''         '..''   '..       .
    #                                 ------------------------------------------------------------
    #                                 -5            '...   .''..'                           '...'    '.    .''...'
    #                                 -10              '.'                                            '.'
    #                                 -15
    #                                     Each point is a frame.

    #                                 The callback must have this signature:
    #                                     frame_processor(indata: numpy.ndarray[frame][channel]) -> bool

    #             timeout (int): number of seconds to record before stopping. If none is set, will run until frame_processor returns False.
    #     """
    #     self._audio_recorder.record_continuous(
    #         frame_processor_callback=frame_processor_callback,
    #         frame_length=frame_length,
    #         samplerate=samplerate,
    #         channels=channels,
    #         timeout=timeout)


    def record_continuous(self,
                        frame_processor_callback: callable,
                        frame_length: int = 1248,
                        samplerate=16000,
                        channels=1,
                        timeout: int = None):
        """ Record audio from the microphone in a continuous loop.
            Args:
                frame_processor_callback (callable->bool): function to pass audio frames to. 
                                    Should accept numpy array of audio data, which is split into channels, and return True if recording should continue. Audio data is split into frames of length frame_length.
                                    A frame is a single point of audio data, represented by an number. Each frame has channels, usually 1 or 2.
                                    audio data is an array of frames.
                                    audio data can be visualized as follows:
                                        audio_data = [frame1, frame2, frame3, ...]
                                        frame1 = [channel1_data, channel2_data, ...]
                                        channel1_data = 60
                                    15       .                          .''.
                                    10     .' .                       .'    '..     .
                                    5    ..'    '.                 .'''         '..''   '..       .
                                    ------------------------------------------------------------
                                    -5            '...   .''..'                           '...'    '.    .''...'
                                    -10              '.'                                            '.'
                                    -15
                                        Each point is a frame.

                                    The callback must have this signature:
                                        frame_processor(indata: numpy.ndarray[frame][channel]) -> bool
                frame_length (int): length of each frame in samples
                samplerate (int): sample rate of the audio. Defaults to 16000.
                channels (int): number of channels
                timeout (int): number of seconds to record before stopping. If none is set, will run until frame_processor returns False.
        """
        self._audio_recorder.record_continuous(
            frame_processor_callback=frame_processor_callback,
            frame_length=frame_length,
            samplerate=samplerate,
            channels=channels,
            timeout=timeout)


    def calibrate_silence(self) -> int:
        """ Calibrate the silence threshold.

        Returns:
            int: The calibrated silence threshold.
        """
        silence_threshold = self._audio_recorder.calibrate_silence()
        return silence_threshold