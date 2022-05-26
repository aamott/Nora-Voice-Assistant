#############################
# Speech to Text Getter
#   - gets an instance of the selected Speech To Text module
#############################
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.core_core.audio_recorder import AudioRecorder

# TODO: Should we move this into audio_utils?


def get_stt_object(stt_module="Stub_STT",
                   settings_tool: SettingsTool = None,
                   channels: Channels = None,
                   audio_recorder: AudioRecorder = None):

    # Get stt type. Current settings override the default.
    module_name = settings_tool.get_setting("default_engine")
    if module_name is None:
        module_name = stt_module
        # Populate the setting if it doesn't already exist.
        settings_tool.set_setting("default_engine", stt_module)

    # Import the selected Speech To Text module
    if module_name == "Stub_STT":
        import core_utils.speech_to_text.stub_stt as stt
    elif module_name == "Google_STT":
        import core_utils.speech_to_text.google_cloud_stt as stt
    elif module_name == "DeepSpeech_STT":
        import core_utils.speech_to_text.deepspeech_stt as stt
    else:
        raise ValueError("Invalid STT type")

    # return an instance of the selected Speech To Text module
    try:
        stt_settings_tool = settings_tool.get_sub_tool(module_name)
        return stt.STT(settings_tool=stt_settings_tool,
                    channels=channels,
                    audio_recorder=audio_recorder)
    except Exception as e:
        # use the fallback text to speech engine
        import core_utils.speech_to_text.stub_stt as fallback_stt
        print("Error:", e)
        stt_settings_tool = settings_tool.get_sub_tool(fallback_stt.STT.name)
        return fallback_stt.STT(settings_tool=stt_settings_tool,
                                channels=channels,
                                audio_recorder=audio_recorder)


if __name__ == "__main__":
    stt = get_stt_object()
    print(stt)