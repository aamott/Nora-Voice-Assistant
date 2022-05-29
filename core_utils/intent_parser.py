###########################
# IntentParser
# The intent parser is responsible for detecting intents.
# It does this by taking a list of skills and asking each one
# to register its intents through the _register_intent function.
# When an intent is detected, sassiness (and other personality traits)
# are calculated and the intent data is returned.
# Core Objects:
#   skills: list of skill objects
#   intents:  Intent Container
###########################
import random
from padaos import IntentContainer
from core_utils.settings_tool import SettingsTool


class IntentParser:

    def __init__(self, skills, settings_tool: SettingsTool):
        """Initialize the IntentParser
        """
        self.settings_tool = settings_tool
        self.skills = skills
        self.intents = IntentContainer()
        self.intent_callbacks = {}

        self.set_up_skills()
        
        # get sass level
        self.sass_level = self.settings_tool.get_setting("sass_level")
        if not self.sass_level:
            self.sass_level = 1
            self.settings_tool.set_setting("sass_level", self.sass_level)

    
    ###########################
    # Personality
    ###########################

    def get_response_sassiness(self) -> int:
        """ Returns the sassiness of the response. Random based on the sass level.
            Returns:
                int: 0-10
        """
        # get a multiplier between 0 and 1
        sass_multiplier = random.uniform(0, 1)
        sassiness: int = int(self.sass_level * sass_multiplier)
        return sassiness

    
    def set_sass_level(self, sass_level: int):
        """Sets the sass level
            Parameters:
                sass_level (int): the sass level to set
        """
        # check that sass_level is between 0 and 10
        self.sass_level = sass_level
        self.settings_tool.set_setting("sass_level", self.sass_level)


    def parse_intent(self, user_input) -> dict:
        """Parses the user input
            Returns:
                dict: the intent and its parameters
                The dict will be in the format:
                    {
                        intent_name: str,
                        entities: {
                            "entity_name": value
                            ...
                        }
                        callback: callable,
                        sassiness: int,
                    }
        """
        intent = self.intents.calc_intent(user_input)
        if intent["name"]:
            # add sassiness to the intent
            intent["sassiness"] = self.get_response_sassiness()
            # add the intent callback (since padaos can't store it)
            intent_callback = self.intent_callbacks[intent["name"]]
            intent["callback"] = intent_callback

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
            except AttributeError:
                print("Skill " + skill.name + " does not have an intent_creator method.")
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