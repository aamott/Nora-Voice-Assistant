###########################
# Records until silence
###########################

import sounddevice as sd
import numpy as np
import time

from scipy.io.wavfile import read, write
import io


class AudioRecorder:

    def __init__(self, samplerate=48000):
        sd.default.samplerate = samplerate
        self.samplerate = sd.default.samplerate

        self.min_threshold = 0
        self.frames_of_silence = 0
        self.recording = False
        self.max_frames_silence = 50  # how many frames of silence before recording stops - filters false silence
        self.recorded_audio = None

    def calibrate_silence(self, samplerate : int = None, channels=1, sample_time=1):
        """ Sample silence for a specified time. Use for auto-adjusting the threshold 
            Args:
                sample_time (int): number of seconds to sample
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
            self.min_threshold = np.max(data[0])

        return self.min_threshold


    def callback(self, indata, num_frames, time, status):
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
        if status:
            print(status)

        max_velocity = np.max(indata)

        if max_velocity > self.min_threshold:
            # print("Speaking...")
            self.frames_of_silence -= 1

        elif max_velocity < self.min_threshold:
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


    def get_recording(self,
               samplerate : int = None,
               channels=1,
               filename=None,
               max_recording_seconds=8) -> np.ndarray:
        """Record audio from the microphone for a specified time.
            Args:
                samplerate (int): sample rate of the audio. Defaults to 48000.
                channels (int): number of channels
                filename (str): filename to save the audio to
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
                                callback=self.callback,
                                samplerate=samplerate,
                                dtype="int16"):
                # wait for recording to finish
                while self.recording:
                    sd.sleep(100)
                    # record for a maximum of max_recording_seconds
                    if time.time() - start_time > max_recording_seconds:
                        self.recording = False

        except Exception as e:
            print("Failed to record:", e)
            raise e

        # flatten the recorded audio
        return self.recorded_audio.flatten()

        # return the recorded audio
        return self.recorded_audio


    def get_recording_as_wav(self,
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
        audio_array = self.get_recording(samplerate=samplerate,
                                            channels=channels,
                                            filename=filename,
                                            max_recording_seconds=max_recording_seconds)

        # convert to wav BytesIO object
        wav_file = io.BytesIO()
        write(wav_file, samplerate, audio_array)
        wav_file.seek(0)
        return wav_file




if __name__ == "__main__":
    recorder = AudioRecorder()

    print("Getting threshold... Shhhh...")
    threshold = recorder.calibrate_silence()

    print("Recording...")
    audio = recorder.get_recording_as_wav().read()

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