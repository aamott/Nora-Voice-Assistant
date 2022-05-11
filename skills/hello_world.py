from skills import base_skill


class Skill(base_skill.Skill):
    name = "Hello World Skill"


    def __init__(self):
        super().__init__()
        self.description = "Hello World"


    def intent_creator(self, register_intent: callable):
        """ registers intents using register_intent """
        register_intent(intent_callback=self.hello_world_intent,
                        intent_phrases=["hello (world | )"],
                        intent_name="say_hello")


    def hello_world_intent(self, intent_data):
        print("Hello World!")
