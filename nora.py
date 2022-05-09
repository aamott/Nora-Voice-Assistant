import core_utils.speech_to_text_getter as stt_getter
import core_utils.intent_parser as intent_parser
import core_utils.skill_getter as skill_getter

# get the STT object
stt = stt_getter.get_stt_object()

# import the skills
skills = skill_getter.import_skills()

# get the intent parser and feed it the skills
intent_parser = intent_parser.IntentParser(skills)

########################################
# main loop
########################################
while True:
    # get the audio
    audio = stt.listen()

    # get the intent
    intent = intent_parser.parse(audio)

    # do something with the intent
    intent()
