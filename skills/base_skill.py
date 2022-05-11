from abc import ABC, abstractmethod

class Skill(ABC):

    def __init__(self):
        """ Initialize the Skill

        """
        pass


    @abstractmethod
    def intent_creator(self, register_intent: callable):
        """ registers intents using register_intent
        """
        pass