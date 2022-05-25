#################################
# NORA
# Nora is a voice assistant built on simplicity.
#################################
from core_utils.core_core.channels import Channels
from core_utils.core_core.settings_manager import SettingsManager
from core_utils.settings_tool import SettingsTool
import core_utils.intent_parser as intent_parser
import core_utils.skill_creator as skill_creator
from core_utils.audio_utils import AudioUtils
from core_utils.wakeword import Wakeword


#######################
# Setup
#######################
channels = Channels()
settings_manager = SettingsManager()

# initialize audio utilities
audio_utils_settings_tool = SettingsTool(settings_manager, setting_path="audio utils")
audio_utils = AudioUtils(settings_tool=audio_utils_settings_tool)

# calibrating audio
print("Calibrating...")
audio_utils.calibrate_silence()
print("Calibration complete!")

# import the skills
skills = skill_creator.import_skills(settings_manager=settings_manager, channels=channels)

# initialize the intent parser
intent_settings_tool = SettingsTool(settings_manager=settings_manager,
                                    setting_path='intent parser')
intent_parser = intent_parser.IntentParser(skills,
                                           settings_tool=intent_settings_tool)

# main callback
def loop():
    """ Main Callback. Processes the user's input and starts a skill."""
    # TODO: play a sound and light up a few RGB LEDs

    # listen for the user's response
    print("Listening...")
    text = audio_utils.listen()
    audio_utils.say("You said: " + text)

    # get the intent
    intent_data = intent_parser.parse_intent(text)

    # run the intent
    if intent_data is not None:
        print("Running intent: " + intent_data["name"])
        intent_data["callback"](intent_data)
    else:
        audio_utils.say("No intent detected")


# initialize wakeword
wakeword_settings_tool = SettingsTool(settings_manager=settings_manager,
                                        setting_path='wakeword.picovoice')
wakeword = Wakeword(settings_tool=wakeword_settings_tool,
                    audio_utils=audio_utils,
                    wakeword_detected_callback=loop)




########################################
# main loop
########################################
audio_utils.say("Hello, I am Nora. I am a virtual assistant.")
while True:
    # TODO: Move wakeword into a separate thread and use a queue (fed by the wakeword_detected_callback)
    # to pass user input to the main thread. Add a lock to recording so that the wakeword doesn't start recording while the user is speaking.
    # wait for wakeword
    wakeword.await_wakeword()