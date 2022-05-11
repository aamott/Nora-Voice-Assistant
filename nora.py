from time import sleep
import core_utils.speech_to_text_getter as stt_getter
import core_utils.intent_parser as intent_parser
import core_utils.skill_creator as skill_creator

# get the STT object - can currently be 'google' or 'deepspeech'
stt = stt_getter.get_stt_object(stt_type="google")

# import the skills
skills = skill_creator.import_skills()

# initialize the intent parser
intent_parser = intent_parser.IntentParser(skills)

# calibrating
print("Calibrating...")
stt.calibrate_audio()

########################################
# main loop
########################################
while True:
    # TODO: Remove when wakeword is implemented
    sleep(1)

    # get the audio
    print("Listening...")
    text = stt.listen()
    print("You said:", text)

    # get the intent
    intent = intent_parser.parse_intent(text)

    # run the intent
    if intent is not None:
        intent["callback"](intent)
    else:
        print("No intent detected")
