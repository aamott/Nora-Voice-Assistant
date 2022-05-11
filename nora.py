from time import sleep
import core_utils.speech_to_text_getter as stt_getter
import core_utils.text_to_speech_getter as tts_getter
import core_utils.intent_parser as intent_parser
import core_utils.skill_creator as skill_creator


# get the STT object - can currently be 'stub', 'google', 'deepspeech'
stt = stt_getter.get_stt_object(stt_type="stub")

# get the TTS object - can currently be 'print', 'google', 'pyttsx3'
tts = tts_getter.get_tts_object(tts_type="pyttsx3")

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
tts.say("Hello, I am Nora. I am a virtual assistant.")
while True:
    # TODO: Remove when wakeword is implemented
    sleep(5)

    # get the audio
    print("Listening...")
    text = stt.listen()
    tts.say("You said: " + text)

    # get the intent
    intent = intent_parser.parse_intent(text)

    # run the intent
    if intent is not None:
        intent["callback"](intent)
    else:
        tts.say("No intent detected")
