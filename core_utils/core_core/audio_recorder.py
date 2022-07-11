###########################
# Audio Recorder
# Contains tools to record audio
# TODO: What if we continually recorded audio,
#       pushed into a queue, and then we read from the queue
#       using callback functions?
#      We could limit the size of the queue to prevent
#     memory issues. It would allow very low latency.
###########################

import sounddevice as sd
import numpy as np
import time

from scipy.io.wavfile import write
import io

from ..settings_tool import SettingsTool


class AudioRecorder:

    def __init__(self,
                 settings_tool: SettingsTool=None,
                 samplerate=48000,
                 channels=1):
        """ Initialize the audio recorder.

            Args:
                settings_tool (SettingsTool): settings tool to use for getting settings
                samplerate (int): sample rate of the audio
                channels (int): number of channels
                max_frames_silence (int): max number of frames of silence detected before recording is stopped
                silence_threshold (int): threshold for silence detection. A good threshold can be
                    determined with the calibrate_silence method.
        """
        self.settings_tool = settings_tool
        sd.default.samplerate = samplerate
        sd.default.channels = channels
        self.samplerate = sd.default.samplerate

        # anything below this threshold is considered silence
        self.silence_threshold = 0

        # how many frames of silence before recording stops - filters false silence
        if self.settings_tool:
            self.max_frames_silence = settings_tool.get_setting("Max Frames of Silence", default=50)
        else:
            self.max_frames_silence = 50

        # current number of frames of silence - starts at 0
        self.frames_of_silence = 0
        self.recording = False
        self.recorded_audio = None


    def calibrate_silence(self, samplerate : int = None, channels=1, sample_time=1, threshold_multiplier=None):
        """ Sample silence for a specified time. Use for auto-adjusting the threshold 

            Args:
                samplerate (int): sample rate of the audio
                channels (int): number of channels
                sample_time (int): number of seconds to sample
                threshold_multiplier (float): multiplier to adjust the threshold by. Make 
                    bigger to make recording stop sooner, smaller to make recording stop later.
            Returns:
                int: silence threshold
        """
        if not samplerate:
            samplerate = self.samplerate

        with sd.InputStream(
                channels=channels,
                # samplerate=self.default_samplerate,
                dtype="int16") as stream:
            data = stream.read(sample_time * self.samplerate)
            self.silence_threshold = np.max(data[0])

        # multiply silence threshold by a factor to account for differences in microphone sensitivity
        if threshold_multiplier:
            self.silence_threshold *= threshold_multiplier
        else:
            if self.settings_tool:
                self.silence_threshold *= self.settings_tool.get_setting("Silence Threshold Multiplier", default=1.0)
            else:
                self.silence_threshold *= 1.0
        return self.silence_threshold


    def _process_frame(self, indata, num_frames, time, status):
        """ This is called (from a separate thread) for each audio block.
            It adds audio to the recorded_audio buffer. If speaking isn't detected
            above the threshold for enough frames, it will send the recording kill signal (self.recording = False).

            As speech is detected, it decreases the number of frames of silence detected until a minimum
            of 0. If the number of frames of silence is greater than the max_frames_silence,
            it will send the recording kill signal (self.recording = False).

        Args:
            indata (ndarray): audio data this block
            num_frames (int): number of frames in this block
            time (CData): PortAudio timestamp (for things like synchronizing MIDI and such)
            status (CallbackFlags): PortAudio status flags
        """
        # TODO: If average volume of a block is less than half(?)
        #           of the average volume of the whole, it is probably silence.
        #           Readjust threshold.
        # if status:
        #     print(status)

        max_velocity = np.max(indata)

        if max_velocity > self.silence_threshold:
            # print("Speaking...")
            self.frames_of_silence -= 1

        elif max_velocity < self.silence_threshold:
            # print("Not speaking...")
            self.frames_of_silence += 1
            # stop recording if silence has been detected for a while
            if self.frames_of_silence > self.max_frames_silence:
                self.recording = False

        if self.frames_of_silence < 0:
            self.frames_of_silence = 0

        # Add audio to the buffer
        if self.recorded_audio is None:
            self.recorded_audio = indata
        else:
            self.recorded_audio = np.concatenate([self.recorded_audio, indata], axis=0)


    def record_until_silence(self,
               samplerate : int = None,
               channels=1,
               filename=None,
               max_recording_seconds=8) -> np.ndarray:
        """Record audio from the microphone for a specified time or until silence is detected.

            Args:
                samplerate (int): sample rate of the audio. Defaults to 48000.
                channels (int): number of channels
                filename (str): filename to save the audio to (not implemented) - TODO
                max_recording_seconds (int): maximum number of seconds to record

            Returns:
                ndarray [int16]: audio data
        """
        if not samplerate:
            samplerate = self.samplerate

        # reset values for recording
        self.frames_of_silence = 0
        self.recorded_audio = None
        start_time = time.time()
        self.recording = True

        try:
            # try to start the recording
            with sd.InputStream(channels=channels,
                                callback=self._process_frame,
                                samplerate=samplerate,
                                dtype="int16"):
                # wait for recording to finish
                while self.recording:
                    sd.sleep(100)
                    # record for a maximum of max_recording_seconds
                    if time.time() - start_time > max_recording_seconds:
                        self.recording = False

                # reset frames_of_silence
                self.frames_of_silence = 0

        except Exception as e:
            print("Failed to record:", e)
            raise e

        # flatten the recorded audio and return it
        return self.recorded_audio.flatten()


    def record_until_silence_as_wav(self,
                                samplerate=48000,
                                channels=1,
                                filename=None,
                                max_recording_seconds=8):
        """Record audio from the microphone for a specified time.

            Args:
                samplerate (int): sample rate of the audio
                channels (int): number of channels
                filename (str): filename to save the audio to
                max_recording_seconds (int): maximum number of seconds to record

            Returns:
                BytesIO: audio data wav file as a BytesIO object. Can be treated like a file.
        """
        audio_array = self.record_until_silence(samplerate=samplerate,
                                            channels=channels,
                                            filename=filename,
                                            max_recording_seconds=max_recording_seconds)

        # convert to wav BytesIO object
        wav_file = io.BytesIO()
        write(wav_file, samplerate, audio_array)
        wav_file.seek(0)
        return wav_file


    # def record_continuous_using_callback(self,
    #                       frame_processor_callback: callable,
    #                       frame_length: int = 1248,
    #                       samplerate=16000,
    #                       channels=1,
    #                       timeout: int = None):
    #     """ Record audio from the microphone in a continuous loop.
    #         Args:
    #             frame_processor (callable->bool): function to pass audio frames to.
    #                                 Should accept numpy array of audio data and return True if done recording.
    #                                 The callback must have this signature:
    #                                     frame_processor(indata: numpy.ndarray) -> bool

    #             timeout (int): number of seconds to record before stopping. If none is set, will run until frame_processor returns False.
    #     """
    #     done_recording = False

    #     # Create callback function that accepts audio frames and sets processing flag to True if recording should continue
    #     def process_frame(indata, num_frames, time, status):
    #         nonlocal done_recording
    #         if not done_recording:
    #             done_recording = frame_processor_callback(indata)
    #         return done_recording

    #     timeout_time = time.time() + timeout if timeout else None


    #     # Start recording
    #     with sd.InputStream(callback=process_frame,
    #                         samplerate=samplerate or self.samplerate,
    #                         dtype="int16",
    #                         blocksize=frame_length,
    #                         channels=channels
    #                         ) as stream:
    #         stream.start()
    #         # Wait for timeout or until recording is stopped
    #         while not done_recording:
    #             # check timeout
    #             if timeout_time and time.time() - timeout > timeout_time:
    #                 break
    #             time.sleep(0.1)


    def record_continuous(self,
                          frame_processor_callback: callable,
                          frame_length: int = 1248,
                          samplerate=16000,
                          channels=1,
                          timeout: int = None):
        """ Record audio from the microphone in a continuous loop.

            Args:
                frame_processor (callable->bool): function to pass audio frames to.
                                    Should accept numpy array of audio data and return True if done recording.
                                    The callback must have this signature:
                                        frame_processor(indata: numpy.ndarray) -> bool
                frame_length (int): number of frames to record per iteration
                samplerate (int): sample rate of the audio
                channels (int): number of channels
                timeout (int): number of seconds to record before stopping. If none is set, will run until frame_processor returns False.
        """
        with sd.InputStream(samplerate=samplerate or self.samplerate,
                            dtype="int16",
                            blocksize=frame_length,
                            channels=channels
                            ) as stream:
            while True:
                # process
                data, _ = stream.read(frame_length)
                if frame_processor_callback(data): #returns true if done recording
                    break



if __name__ == "__main__":
    recorder = AudioRecorder()

    print("Getting threshold... Shhhh...")
    threshold = recorder.calibrate_silence()

    print("Recording...")
    audio = recorder.record_until_silence_as_wav().read()

    print("Playing the recording...")
    import pygame
    pygame.mixer.init()
    pygame.mixer.music.load(io.BytesIO(audio))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.delay(100)
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    print("Playing the recording array...")
    sd.play(recorder.recorded_audio, 48000)
    sd.wait()
