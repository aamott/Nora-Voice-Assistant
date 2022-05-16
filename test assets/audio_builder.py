######################
# Audio Builder
# Converts audio files into numpy arrays
######################
import numpy as np
import os

def get_audio_array(audio_file_path: str) -> np.ndarray:
    # load audio file
    audio_data = np.fromfile(audio_file_path, dtype=np.int16)
    # convert to mono
    audio_data = np.mean(audio_data.reshape((-1, 2)), axis=1)
    # normalize
    audio_data = audio_data / np.max(np.abs(audio_data))
    return audio_data


if __name__ == "__main__":
    # test audio builder
    audio_file_path = "test_assets/audio_builder.py"
    audio_data = get_audio_array(audio_file_path)
    print(audio_data)