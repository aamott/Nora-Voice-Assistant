#######################
# Hello World Skill
#######################
from skills import base_skill
from core_utils.settings_tool import SettingsTool

class Skill(base_skill.Skill):
    name = "Hello World Skill"


    def __init__(self, settings_tool: SettingsTool):
        super().__init__()
        self.settings_tool = settings_tool


    def intent_creator(self, register_intent: callable):
        """ registers intents using register_intent """
        register_intent(intent_callback=self.hello_world_intent,
                        intent_phrases=["hello (world | )"],
                        intent_name="say_hello")


    def hello_world_intent(self, intent_data):
        print("Hello World!")
