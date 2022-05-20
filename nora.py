#################################
# NORA
# Nora is a voice assistant built on simplicity.
#################################
from time import sleep
from core_utils.core_core.settings_manager import SettingsManager
from core_utils.settings_tool import SettingsTool
import core_utils.intent_parser as intent_parser
import core_utils.skill_creator as skill_creator
from core_utils.audio_utils import AudioUtils


#######################
# Setup
#######################
settings_manager = SettingsManager()

audio_utils_settings_tool = SettingsTool(settings_manager, setting_path="audio utils")
audio_utils = AudioUtils(settings_tool=audio_utils_settings_tool)

# import the skills
skills = skill_creator.import_skills(settings_manager=settings_manager)

# initialize the intent parser
intent_settings_tool = SettingsTool(settings_manager=settings_manager,
                                    setting_path='intent parser')
intent_parser = intent_parser.IntentParser(skills,
                                           settings_tool=intent_settings_tool)

# calibrating
print("Calibrating... Shhh...")
audio_utils.calibrate_silence()
print("Calibrated!")


########################################
# main loop
########################################
audio_utils.say("Hello, I am Nora. I am a virtual assistant.")
while True:
    # TODO: Remove when wakeword is implemented
    sleep(5)

    # get the audio
    print("Listening...")
    text = audio_utils.listen()
    audio_utils.say("You said: " + text)

    # get the intent
    intent = intent_parser.parse_intent(text)

    # run the intent
    if intent is not None:
        intent["callback"](intent)
    else:
        audio_utils.say("No intent detected")
