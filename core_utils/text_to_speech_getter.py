#############################
# Text to Speech Getter
#   - gets an instance of the selected Text to Speech module
#############################


# TODO: Should we move this into audio_utils?
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool


def get_tts_object(tts_module="print",
                   channels: Channels = None,
                   settings_tool: SettingsTool = None):

    # Get tts type. Current settings override the default.
    module_name = settings_tool.get_setting("default_engine")
    if module_name is None:
        module_name = tts_module
        # Populate the setting if it doesn't already exist.
        settings_tool.set_setting("default_engine", tts_module)

    # Import the selected Text to Speech module
    try: 
        if module_name == "Print":
            import core_utils.text_to_speech.command_line_tts as tts
        elif module_name == "Google_TTS":
            import core_utils.text_to_speech.google_tts as tts
        elif module_name == "pyttsx3_TTS":
            import core_utils.text_to_speech.pyttsx3_tts as tts
        elif module_name == "MS_Voice_TTS":
            import core_utils.text_to_speech.microsoft_tts as tts
        else:
            raise ValueError("Invalid TTS type: ", module_name)

        # return an instance of the selected Text to Speech module
        tts_settings_tool = settings_tool.get_sub_tool(tts.TTS.name)
        return tts.TTS(channels=channels, settings_tool=tts_settings_tool)
        
    except Exception as e:
        # use the fallback text to speech engine
        import core_utils.text_to_speech.pyttsx3_tts as fallback_tts
        print("Error:", e)
        tts_settings_tool = settings_tool.get_sub_tool(fallback_tts.TTS.name)
        return fallback_tts.TTS(channels=channels,
                                settings_tool=tts_settings_tool)

if __name__ == "__main__":
    tts = get_tts_object()
    print(tts)