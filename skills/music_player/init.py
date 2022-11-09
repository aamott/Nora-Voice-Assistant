###########################
# Music Player Skill
###########################
from atexit import register
from multiprocessing.spawn import import_main_path
from skills import base_skill
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.audio_utils import AudioUtils
import os
from pathlib import Path
from .song_manager import SongDatabase


class Skill(base_skill.BaseSkill):
    name = "Music Player Skill"


    def __init__(self, settings_tool: SettingsTool, channels: Channels, audio_utils: AudioUtils):
        self.settings_tool = settings_tool
        self.channels = channels
        self.audio_utils = audio_utils

        # Populate the settings tool. This only needs to be done once so the user has a setting to change.
        self.settings_tool.create_setting("music folder", default_value=str(Path.home()) + "/Music" )

        # Initialize the song database
        folder = self.settings_tool.get_setting("music folder")
        if folder is None:
            # Use the Music folder in the user's home directory if no folder is set.
            self.folder = str(Path.home()) + "/Music"
            self.settings_tool.set_setting("music folder", folder)

        # check that the folder exists
        if not os.path.exists(folder):
            self.audio_utils.say("The currently selected music folder doesn't exist. Please set it in the settings.")
            raise Exception("Music path does not exist.")

        supported_music_filetypes = [".mp3", ".wav", ".ogg"] # This can be removed if we use a fully featured music player.

        print("Loading Music Directory: ", folder)
        self.song_manager = SongDatabase(music_dir=folder, music_extensions=supported_music_filetypes)



    def intent_creator(self, register_intent: callable):
        """ This function registers intents using register_intent.
            Parameters: 
                register_intent (callable): a function that can add an intent to Nora. """

        # register another intent to say hello to a specific name
        register_intent(
                    intent_callback= self.play_song_intent,
                    # We can add 'entities' (which are like parameters) to the intent.
                    intent_phrases=["Play {song}", "Start {song}"],
                    intent_name="Music_Player"
                    )
        register_intent(
            intent_callback= self.music_pause,
                    
                    intent_phrases=["pause", "pause (the | ) music"],
                    
                    intent_name="music_pause"
                    )
        register_intent(
            intent_callback= self.music_resume,
                    
                    intent_phrases=["Resume (music | )", "Play (the music| music)"],
                    
                    intent_name="music_resume"
                    )
        register_intent(
            intent_callback= self.music_stop,
                    
                    intent_phrases=["Stop (music | )", "stop (the music| )"],
                    
                    intent_name="music_stop"
                    )
        register_intent(
            intent_callback= self.decrease_volume,
                    
                    intent_phrases=["lower (the | ) volume", "decrease (the | ) volume"],
                    
                    intent_name="decrease volume"
                    )
        register_intent(
            intent_callback= self.increase_volume,
                    
                    intent_phrases=["increase (the | ) volume", "up (the | ) volume"],
                    
                    intent_name="increase volume"
                    )
        register_intent(
            intent_callback= self.max_volume,
                    
                    intent_phrases=["max volume"],
                    
                    intent_name="max volume"
                    )           
        register_intent(
            intent_callback= self.mmin_volume,
                    
                    intent_phrases=["lowest volume", "(min| minimum) volume"],
                    
                    intent_name="min volume"
                    ) 
    
    
    def play_song_intent(self, intent_data):
        """ Plays a song from the song database. """
        # intent_data looks like this:
        # {'name': 'add_item', 'entities': {'song': 'song choice'}}

        song_request = intent_data["entities"].get("song")

        matching_songs = self.song_manager.search_songs(song_request, confidence_threshold=0.2)

        if len(matching_songs) == 0:
            self.audio_utils.say("I couldn't find that song.")
            return

        top_song, confidence = matching_songs[0]

        # Play the song
        self.audio_utils.play(top_song["filepath"])
        self.audio_utils.say("Playing " + top_song["title"])

    def music_pause(self, intent_data):
       self.audio_utils.pause()
    
    def music_resume(self, intent_data):
       self.audio_utils.resume()

    def music_stop(self, intent_data):
       self.audio_utils.stop()
    
    def decrease_volume(self, intent_data):
       self.audio_utils.decrease_volume()
    
    def increase_volume(self, intent_data):
       self.audio_utils.increase_volume()
    
    def max_volume(self, intent_data):
        self.audio_utils.max_volume()
    
    def min_volume(self, intent_data):
        self.audio_utils.min_volume()