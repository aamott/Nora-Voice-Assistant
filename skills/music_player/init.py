###########################
# Music Player Skill
###########################
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
        self.settings_tool.create_setting("music folder")

        # Initialize the song database
        folder = self.settings_tool.get_setting("music folder")
        if folder is None:
            # Use the Music folder in the user's home directory if no folder is set.
            self.folder = str(Path.home()) + "/Music"
            self.settings_tool.set_setting("music folder", folder)

        # check that the folder exists
        if not os.path.exists(folder):
            self.audio_utils.say("The current music folder doesn't exist. Please set it in the settings.")
            return

        supported_music_filetypes = [".mp3", ".wav", ".ogg"] # This can be removed if we use a fully featured music player.
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
