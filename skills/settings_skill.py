#######################
# Settings Skill
# Used to manage some - not all - settings.
#######################
from skills import base_skill
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.audio_utils import AudioUtils


class Skill(base_skill.BaseSkill):
    name = "Settings Skill"

    def __init__(self, settings_tool: SettingsTool, channels: Channels,
                 audio_utils: AudioUtils):
        self.settings_tool = settings_tool
        self.channels = channels
        self.audio_utils = audio_utils


    def intent_creator(self, register_intent: callable):
        """ registers intents using register_intent """
        intent_phrases = ["set ( sass | sassiness) (level | ) to {sassiness} (percent | )" ]
        callback = self.update_sass
        register_intent(intent_callback=callback,
                        intent_phrases=intent_phrases,
                        intent_name="update_sass")


    def update_sass(self, intent_data):
        """ update sassiness levels"""
        sassiness = intent_data.get("sassiness")
        try:
            sassiness = int(sassiness)
        except ValueError:
            self.audio_utils.say("I don't know how to set sassiness to {}".format(sassiness))
            return

        # If percent is in the user's phrase, set the range to 0-100
        if intent_data.get("user_phrase").find("percent") > -1:
            sassiness = sassiness / 10

        # set sassiness within bounds
        if sassiness < 0:
            sassiness = 0
        elif sassiness > 10:
            sassiness = 10
        if sassiness == 10:
            self.audio_utils.say("Warning: Sassiness set to critical levels. May cause severe burns.")
        else:
            self.audio_utils.say("Setting sassiness to " + str(sassiness))
        self.channels.publish("set_sass_level", sassiness)