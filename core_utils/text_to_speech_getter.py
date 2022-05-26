#############################
# Text to Speech Getter
#   - gets an instance of the selected Text to Speech module
#############################


# TODO: Should we move this into audio_utils?
def get_tts_object(tts_module="print", channels=None, settings_tool=None):
    # TODO: get settings for TTS
    tts_module = settings_tool.get_setting("tts_module") or tts_module

    # Import the selected Text to Speech module
    if tts_module == "print":
        import core_utils.text_to_speech.command_line_tts as TTS
    elif tts_module == "google":
        import core_utils.text_to_speech.google_tts as TTS
    elif tts_module == "pyttsx3":
        import core_utils.text_to_speech.pyttsx3_tts as TTS
    else:
        raise ValueError("Invalid TTS type")

    # return an instance of the selected Text to Speech module
    tts_settings_tool = settings_tool.get_sub_tool("text_to_speech")
    return TTS.TTS(channels=channels, settings_tool=tts_settings_tool)


if __name__ == "__main__":
    tts = get_tts_object()
    print(tts)