from skills import base_skill


class Skill(base_skill.Skill):
    name = "Hello World"

    def __init__(self):
        super().__init__()
        self.description = "Hello World"


    def intent_creator(self, register_intent: callable):
        """ registers intents using register_intent
        """
        # TODO: register intents
        pass