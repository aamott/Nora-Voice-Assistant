#############################
# Speech to Text Getter
#   - gets an instance of the selected Speech To Text module
#############################


def get_stt_object(stt_type="stub"):
    # TODO: get settings for STT
    # stt_type = settings.get_setting("stt_type")

    # Import the selected Speech To Text module
    if stt_type == "stub":
        import core_utils.speech_to_text.stub_stt as STT
    elif stt_type == "google":
        import core_utils.speech_to_text.google_cloud_stt as STT
    elif stt_type == "deepspeech":
        import core_utils.speech_to_text.deepspeech_stt as STT
    else:
        raise ValueError("Invalid STT type")

    # return an instance of the selected Speech To Text module
    return STT.STT()


if __name__ == "__main__":
    stt = get_stt_object()
    print(stt)