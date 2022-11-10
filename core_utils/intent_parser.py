####################
# IntentParser
# Core Objects:
#   skills: list of skill objects
#   intents:  Intent Container
####################
from padaos import IntentContainer
from .core_core.channels import Channels
from .settings_tool import SettingsTool


class IntentParser:

    def __init__(self, skills, settings_tool: SettingsTool, channels: Channels):
        """Initialize the IntentParser
        """
        self.settings_tool = settings_tool
        self.skills = skills
        self.intents = IntentContainer()
        self.intent_callbacks = {}

        self.set_up_skills()


    def parse_intent(self, user_input) -> dict:
        """Parses the user input

            Returns:
                intent ( {'name':str, 'original_phrase':str 'callback':callable, 'entities': {'<entity_name>': value}} )
                    or None if no intent is detected
        """
        intent = self.intents.calc_intent(user_input)
        if intent.get("name"):
            try:
                # add the intent callback (since padaos can't store it)
                intent_callback = self.intent_callbacks[intent["name"]]
                intent["original_phrase"] = user_input
                intent["callback"] = intent_callback
            
            except Exception as e:
                print("Error on intent callback: " + str(e))
                intent = None

            return intent
        else:
            return None



    def set_up_skills(self):
        """Sets up the skills
            Calls the intent_creator method for each skill, passing in a 
            register_intent function customized for that skill's name.
        """
        for skill in self.skills:

            # Create a custom register_intents function with the skill name already in place.
            # We need this because the intent parser needs all names to be unique,
            # but the intents may not all be unique, so we concatenate the skill name and the
            # intent name.
            def register_intent_skill(intent_callback : callable, intent_phrases : list[str], intent_name : str):
                """Registers an intent for a skill

                Args:
                    intent_callback (callable): the function to be called when the intent is detected
                    intent_phrases (list): the phrases to be recognized (formatted for
                                                    the selected intent_parser)
                    intent_name (str): The name of the intent. Must be uniqe in the skill.
                """
                unique_intent_name = skill.name + "." + intent_name
                self._register_intent(intent_callback,
                                      intent_phrases,
                                      intent_name=unique_intent_name)

            # Tell the skill to register its intents
            try:
                skill.intent_creator(register_intent_skill)
            except AttributeError as e:
                print("Skill " + skill.name + " does not have an intent_creator method or it crashed.")
                print("Error: ", e)
            except Exception as e:
                print("Error registering intents for skill " + skill.name + ": " + str(e))



    #############
    # Helper functions
    #############

    def _register_intent(self, intent_callback: callable, intent_phrases: list[str], intent_name : str):
        """ Registers an intent
        
            Parameters:
                intent_callback (callable): the function to be called when the intent is detected
                intent_phrases (list): the phrases to be recognized, (formatted for 
                                        the selected intent_parser)
                intent_name (str): the name of the intent (must be unique in the system)
        """
        self.intents.add_intent(intent_name, intent_phrases)
        self.intent_callbacks[intent_name] = intent_callback



##########################################
# Testing
##########################################
if __name__ == "__main__":
    ################
    # Example Skill
    class Skill:
        name = "Hello World"

        def __init__(self):
            super().__init__()

        def intent_creator(self, register_intent: callable):
            """ registers intents using register_intent
            """
            register_intent(intent_callback=self.hello_world_intent, intent_phrases=["hello (world | )"], intent_name="say_hello")

        def hello_world_intent(self, intent_data):
            print("Hello World!")


    intent_parser = IntentParser( [Skill()] )


    # Test the intent parser
    intent = intent_parser.parse_intent("hello world")
    print("Intent for hello world:", intent)
    intent["callback"](intent)

    intent = intent_parser.parse_intent("hello")
    print("Intent for hello:", intent)
    intent["callback"](intent)