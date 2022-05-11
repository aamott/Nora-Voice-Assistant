#############################
# Text to Speech Getter
#   - gets an instance of the selected Speech To Text module
#############################


def get_tts_object(tts_type="stub"):
    # TODO: get settings for TTS
    # tts_type = settings.get_setting("tts_type")

    # Import the selected Speech To Text module
    if tts_type == "stub":
        import core_utils.text_to_speech.command_line_tts as TTS
    elif tts_type == "google":
        import core_utils.text_to_speech.google_tts as TTS
    elif tts_type == "pyttsx3":
        import core_utils.text_to_speech.pyttsx3_tts as TTS
    else:
        raise ValueError("Invalid TTS type")

    # return an instance of the selected Speech To Text module
    return TTS.TTS()


if __name__ == "__main__":
    tts = get_tts_object()
    print(tts)