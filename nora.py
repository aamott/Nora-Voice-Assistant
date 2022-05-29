#########################################
# NORA
# Nora is a voice assistant built on simplicity.
# Commands are added to a queue by by the user giving a verbal
# command (ex. "Nora, what's the weather?") or via the web
# interface. Commands are processed in the order received.
#########################################
from core_utils.core_core.channels import Channels
from core_utils.core_core.settings_manager import SettingsManager
from core_utils.settings_tool import SettingsTool
import core_utils.intent_parser as intent_parser
import core_utils.skill_creator as skill_creator
from core_utils.audio_utils import AudioUtils
from core_utils.wakeword import Wakeword

from threading import Thread, Event
import queue


#######################
# Threading
#######################
speech_queue = queue.Queue()
shutdown_event = Event()


def consume_input():
    """ Consumes the input from the queue. 
    Returns True if the exit command was received. """
    text = speech_queue.get()
    if shutdown_event.is_set():
        return
    intent_data = intent_parser.parse_intent(text)

    # run the intent
    if intent_data is not None:
        intent_data["callback"](intent_data)
    else:
        audio_utils.say("No intent detected")


def await_wakeword_thread():
    """ Thread for the wakeword. """
    while not shutdown_event.is_set():
        wakeword.await_wakeword()
        # TODO: find a more immediate way to kill the thread.
        #  It currently waits until await_wakeword is done running.
        if shutdown_event.is_set():
            break

        print("Listening...")
        text = audio_utils.listen()
        if text is not None:
            print("You said: " + text)
            speech_queue.put(text)


def shutdown_system():
    """ Shuts down the system. """
    print("Save settings")
    settings_manager.save_settings()
    print("Shutting down...")
    audio_utils.say("Shutting down")
    print(shutdown_event.is_set())
    shutdown_event.set()



#######################
# Setup
#######################
channels = Channels()
settings_manager = SettingsManager()

# initialize audio utilities
audio_utils_settings_tool = SettingsTool(settings_manager, setting_path="audio_utils")
audio_utils = AudioUtils(settings_tool=audio_utils_settings_tool, channels=channels)

# import the skills
skills = skill_creator.import_skills(settings_manager=settings_manager, channels=channels, audio_utils=audio_utils)

# initialize the intent parser
intent_settings_tool = SettingsTool(settings_manager=settings_manager,
                                    setting_path='intent parser')
intent_parser = intent_parser.IntentParser(skills,
                                           settings_tool=intent_settings_tool, channels=channels,)

# initialize wakeword
wakeword_settings_tool = SettingsTool(settings_manager=settings_manager,
                                        setting_path='wakeword.picovoice')
wakeword = Wakeword(settings_tool=wakeword_settings_tool,
                    audio_utils=audio_utils)


channels.subscribe(shutdown_system, "shutdown")

# calibrating audio
print("Calibrating...")
audio_utils.calibrate_silence()
print("Calibration complete!")


# CTRL+C handler
import signal
import sys

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    shutdown_system()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

########################################
# main loop
########################################
# startup fanciness
audio_utils.say("Hello, I am Nora. I am a virtual assistant.")

# start the wakeword thread
wakeword_thread = Thread(target=await_wakeword_thread)
wakeword_thread.start()

# start the main loop
while not shutdown_event.is_set():
    consume_input()

# stop any system threads
wakeword_thread.join(1)