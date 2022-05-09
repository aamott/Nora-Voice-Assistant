import core_utils.speech_to_text_getter as stt_getter
import core_utils.intent_parser as intent_parser

# get the STT object
stt = stt_getter.get_stt_object()

print("Speech Engine:", stt.name)
# choose a skill
intent_parser = intent_parser.IntentParser()

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
