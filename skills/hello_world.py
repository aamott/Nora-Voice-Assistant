###################################
# Hello World Skill
# This skill serves as an example of how to create a skill.
# To create your own skill, copy this file and modify it
# to fit your needs.
###################################
from skills import base_skill
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.audio_utils import AudioUtils

class Skill(base_skill.BaseSkill):
    name = "Hello World Skill"


    def __init__(self, settings_tool: SettingsTool, channels: Channels, audio_utils: AudioUtils):
        """ Initialize the skill. Don't remove any of the existing code, 
            but feel free to add your own. """
        self.settings_tool = settings_tool
        self.channels = channels
        self.audio_utils = audio_utils


    def intent_creator(self, register_intent: callable):
        """ This function registers intents using register_intent.
            Parameters: 
                register_intent (callable): a function that can add an intent to Nora. """
        # register an intent to say "Hello world!" when the user says "hello" or "hello world"
        register_intent(
                        # The intent callback is the function that is called when the intent is detected.
                        intent_callback=self.hello_world_intent,
                        # The intent phrase that will be recognized.
                        # Here, it will match 'hello world' or 'hello'.
                        intent_phrases=["Hello (world | )"],
                        # The intent name. This is used to identify the intent.
                        # Good practice is to use a name like your function name.
                        intent_name="say_hello")

        # register another intent to say hello to a specific name
        register_intent(intent_callback=self.hello_user_intent,
                        # We can add 'entities' (which are like parameters) to the intent.
                        intent_phrases=["Hello. My name is {name}"],
                        intent_name="say_hello_name")


    def hello_world_intent(self, intent_data):
        """This is the function that is called when the intent is detected."""
        print("Hello World!")
        self.audio_utils.say("Hello World!")


    def hello_user_intent(self, intent_data):
        """This is a slightly fancier version of the hello world intent.
            It takes a name as a parameter and says hello to that name."""
        # intent_data looks like this:
        # {'name': 'add_item', 'entities': {'item': 'potatoes', 'list_name': 'shopping'}}
        name = intent_data["entities"].get("name")

        print("Hello " + name + "!")
        self.audio_utils.say("Hello " + name + "!")