import core_utils.speech_to_text_getter as stt_getter
import core_utils.intent_parser as intent_parser
import core_utils.skill_creator as skill_creator

# get the STT object
stt = stt_getter.get_stt_object()

# import the skills
skills = skill_creator.import_skills()

# initialize the intent parser
intent_parser = intent_parser.IntentParser(skills)

########################################
# main loop
########################################
while True:
    # get the audio
    audio = stt.listen()

    # get the intent
    intent = intent_parser.parse_intent(audio)

    # run the intent
    intent()
