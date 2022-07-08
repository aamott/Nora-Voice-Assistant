###########################
# Music Player Skill
###########################
from distutils.log import error
from multiprocessing.spawn import import_main_path
from skills import base_skill
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.audio_utils import AudioUtils
import os
from pathlib import Path



class Skill(base_skill.BaseSkill):
    name = "Music Player Skill"
   

    def __init__(self, settings_tool: SettingsTool, channels: Channels, audio_utils: AudioUtils):
        """ Initialize the skill. Don't remove any of the existing code, 
            but feel free to add your own. """
        self.settings_tool = settings_tool
        self.channels = channels
        self.audio_utils = audio_utils

        self.folder = self.settings_tool.get_setting("music folder")
        if self.folder is None:
            self.folder = (r"C:\Users\Capta\Music")
            self.settings_tool.set_setting("music folder", self.folder)
        
        # iterate through music folder recursively and add all songs to the dictionary



    def intent_creator(self, register_intent: callable):
        """ This function registers intents using register_intent.
            Parameters: 
                register_intent (callable): a function that can add an intent to Nora. """
      

        # register another intent to say hello to a specific name
        register_intent(
                    intent_callback= self.music_player_intent,
                    # We can add 'entities' (which are like parameters) to the intent.
                    intent_phrases=["Play {music}", "Start {music}}"],
                    intent_name="Music_Player"
                    )

    def music_player_intent(self, intent_data):
        """This is a slightly fancier version of the hello world intent.
            It takes a name as a parameter and says hello to that name."""
        # intent_data looks like this:
        # {'name': 'add_item', 'entities': {'item': 'potatoes', 'list_name': 'shopping'}}

        song = intent_data["entities"].get("music")
       
        path = (r"C:\Users\Capta\Music")

        self.audio_utils.say("Playing")

        self.audio_utils.play_song(path, song)



        
       

