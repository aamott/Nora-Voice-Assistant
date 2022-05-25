############################
# Wakeword
# This class is used to detect the wakeword
# When the wakeword is detected, the wakeword_detected function is called
# The wakeword_detected function should call the wakeword_detected_callback function
############################
# Code for testing by running this file directly:
if __name__ == "__main__":
    import sys
    import os
    # Add parent directory to path so we can import the core_utils package
    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)

import pvporcupine
from core_utils.audio_utils import AudioUtils
from core_utils.core_core.settings_manager import SettingsManager
from core_utils.settings_tool import SettingsTool


class Wakeword:

    def __init__(self, settings_tool: SettingsTool, audio_utils: AudioUtils,
                 wakeword_detected_callback: callable = None):
        self.settings_tool = settings_tool
        self.audio_utils = audio_utils
        self.wakeword_detected_callback = wakeword_detected_callback

        # load the settings
        key = self.settings_tool.get_setting("key")
        sensitivities = self.settings_tool.get_setting("sensitivities")
        keywords = self.settings_tool.get_setting("keywords")

        # validate the settings
        if key is None:
            self.settings_tool.set_setting("key", None) # add a place to put a key
            raise ValueError("key is not set")
        if sensitivities is None:
            sensitivities = [0.5]
        if keywords is None:
            self.settings_tool.set_setting("keywords", None)
            keywords = ["picovoice"]

        # load the wakeword
        self.porcupine = pvporcupine.create(access_key=key,
                                            keywords=['picovoice'],
                                            sensitivities=sensitivities,)
        if self.porcupine is None:
            raise Exception("Failed to load porcupine using API key: " + key)


    def wait_for_wakeword_callback(self, audio_data) -> bool:
        """ Callback function for wakeword detection. This function will be passed to the AudioRecorder.
            When the wakeword is detected, the wakeword_detected_callback function will be called.
            Args:
                audio_data (ndarray): The audio data to process.
            Returns:
                bool: Whether the wakeword was detected and recording is done. True if recording is done.
        """
        # method 1 of flattening and sending only one channel
        audio_data = audio_data.transpose()[0]

        # method 2 of flattening and sending only one channel
        # audio_data = audio_data.flatten()  # only works for mono

        # process the audio data
        keyword_index = self.porcupine.process(audio_data)

        # if wakeword was detected
        if keyword_index >= 0:
            # call the wakeword_detected_callback
            if self.wakeword_detected_callback is not None:
                self.wakeword_detected_callback()
            return True
        else:
            return False


    def await_wakeword(self, timeout: int = None):
        """ Await wakeword.
        """
        # wait for wakeword. Record continously until wakeword is detected.
        self.audio_utils.record_continuous(
            frame_processor_callback=self.wait_for_wakeword_callback,
            frame_length=512,
            samplerate=16000,
            channels=1,
            timeout=timeout)


    def __del__(self):
        self.porcupine.delete()



if __name__ == "__main__":
    # test the wakeword
    settings_manager = SettingsManager()
    settings_tool = SettingsTool(settings_manager=settings_manager,
                                 setting_path="wakeword.picovoice")
    audio_utils = AudioUtils(settings_tool=settings_tool)
    wakeword_detected_callback = lambda: print("Wakeword detected!")

    wakeword = Wakeword(settings_tool, audio_utils, wakeword_detected_callback)
    wakeword.await_wakeword()