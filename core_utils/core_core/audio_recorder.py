###########################
# Records until silence
###########################

import sounddevice as sd
import numpy as np
import time

from scipy.io.wavfile import read, write
import io


class AudioRecorder:

    def __init__(self):
        self.min_threshold = 0
        self.frames_of_silence = 0
        self.recording = False

        self.max_frames_silence = 50  # how many frames of silence before recording stops - filters false silence

        self.recorded_audio = None

    def sample_silence(self, samplerate=48000, channels=1, sample_time=1):
        """ Sample silence for a specified time. Use for auto-adjusting the threshold 
            Args:
                samplerate (int): sample rate of the audio
                channels (int): number of channels
                sample_time (int): number of seconds to sample
            Returns:
                ndarray: audio data
        """
        with sd.InputStream(channels=1, samplerate=48000,
                            dtype="int16") as stream:
            data = stream.read(sample_time * samplerate)
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
            print("Speaking...")
            self.frames_of_silence -= 1

        elif max_velocity < self.min_threshold:
            print("Not speaking...")
            self.frames_of_silence += 1
            # stop recording if silence has been detected for a while
            if self.frames_of_silence > self.max_frames_silence:
                self.recording = False

        if self.frames_of_silence < 0:
            self.frames_of_silence = 0

        # Add audio to the buffer
        if self.recorded_audio:
            np.concatenate((self.recorded_audio, indata[0]))
        else:
            self.recorded_audio = indata[0]

    def record(self,
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
                bytes: audio data wav file
        """
        # reset values for recording
        self.frames_of_silence = 0
        self.recorded_audio = None
        start_time = time.time()
        self.recording = True

        try:
            # try to start the recording
            with sd.InputStream(channels=1,
                                callback=self.callback,
                                samplerate=48000,
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

        # Convert frames from numpy array to bytes
        bytes_wav = bytes()
        bytes_io = io.BytesIO(
            bytes_wav)  # create a temporary buffer to store the wav file
        write(bytes_io, samplerate,
              self.recorded_audio)  #write to the bytes object
        output_wav = bytes_io.read()  # and back to bytes

        # save the audio
        if filename:
            with open(filename, 'wb') as f:
                f.write(output_wav)

        # return the bytes object
        return output_wav


if __name__ == "__main__":
    recorder = AudioRecorder()
    threshold = recorder.sample_silence()
    recorder.record()
