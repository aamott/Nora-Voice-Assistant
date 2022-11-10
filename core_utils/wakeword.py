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

from threading import Event
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

        # populate the settings tool
        self.populate_settings()

        # get settings
        key = self.settings_tool.get_setting("key")
        sensitivities = self.settings_tool.get_setting("sensitivities")
        keywords = self.settings_tool.get_setting("keywords")
        keyword_paths = self.settings_tool.get_setting("model_path", default='wakewords/Carmen_en_windows_v2_1_0.ppn')

        # validate the settings
        if key is None:
            raise ValueError("Porcupine API key is not set")

        keywords = keywords or ["picovoice"]
        sensitivities = sensitivities or [0.5]
        if type(keywords) is not list:
            keywords = keywords.to_list()

        # make keyword path None or list
        if keyword_paths is not None and type(keyword_paths) is not list:
            keyword_paths = [keyword_paths]

        if keyword_paths is not None and len(keyword_paths) != len(sensitivities):
            # fill sensitivity list with default values
            sensitivities = [i * sensitivities[0] for i in range(0, len(keyword_paths))]
        elif len(keywords) != len(sensitivities):
            sensitivities = [ i * sensitivities[0] for i in range(0, len(keywords)) ]

        # load the wakeword
        try: 
            # try to load with any custom wakewords
            self.porcupine = pvporcupine.create(access_key=key,
                                                keywords=keywords,
                                                sensitivities=sensitivities,
                                                keyword_paths=keyword_paths)
        except Exception as e:
            # try to load without any custom keywords 
            self.porcupine = pvporcupine.create(access_key=key,
                                    keywords=keywords,
                                    sensitivities=sensitivities)

        if self.porcupine is None:
            raise Exception("Failed to load porcupine using API key: " + key)


    def wait_for_wakeword_callback(self, audio_data) -> bool:
        """ Callback function for wakeword detection. This function will be passed to the AudioRecorder.
            When the wakeword is detected, the wakeword_detected_callback function will be called.
            If the shutdown_event is set, the function will return immediately.

            Args:
                audio_data (ndarray): The audio data to process.
            Returns:
                bool: Whether the wakeword was detected and recording is done. True if recording is done.
        """
        # check if shutdown event is set
        if self.shutdown_event is not None and self.shutdown_event.is_set():
            return True

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


    def await_wakeword(self, timeout: int = None, shutdown_event: Event = None):
        """ Await wakeword.
        
            Args:
                timeout (int): The timeout in seconds. If None, the function will wait indefinitely.
                shutdown_event (Event): The shutdown event. If set, the function will return immediately.
        """

        self.shutdown_event = shutdown_event

        # wait for wakeword. Record continously until wakeword is detected.
        self.audio_utils.record_continuous(
            frame_processor_callback=self.wait_for_wakeword_callback,
            frame_length=512,
            samplerate=16000,
            channels=1,
            timeout=timeout)


    def populate_settings(self):
        """ Populates the settings tool with the settings needed for wakeword.
        """
        self.settings_tool.create_setting("key", None)
        self.settings_tool.create_setting("sensitivities", None)
        self.settings_tool.create_setting("keywords", None)
        self.settings_tool.create_setting("model_path", None)



if __name__ == "__main__":
    # test the wakeword
    settings_manager = SettingsManager()
    settings_tool = SettingsTool(settings_manager=settings_manager,
                                 setting_path="wakeword.picovoice")
    audio_utils = AudioUtils(settings_tool=settings_tool)
    wakeword_detected_callback = lambda: print("Wakeword detected!")

    wakeword = Wakeword(settings_tool, audio_utils, wakeword_detected_callback)
    wakeword.await_wakeword()