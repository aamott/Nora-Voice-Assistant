from padaos import IntentContainer


####################
# IntentParser
# Core Objects:
#   skills: list of skill objects
#   intents:   { skill: { phrases: phrases, callback: skill}}
####################
class IntentParser:

    def __init__(self, skills):
        """Initialize the IntentParser
        """
        self.skills = skills

    def parse_intent(self, user_input):
        # TODO: parse the user input
        pass

    #############
    # Helper functions
    #############

    def register_intent(self, intent_callback: callable, intent_phrases: list):
        pass
