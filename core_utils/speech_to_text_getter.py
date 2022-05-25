#############################
# Speech to Text Getter
#   - gets an instance of the selected Speech To Text module
#############################
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.core_core.audio_recorder import AudioRecorder

# TODO: Should we move this into audio_utils?


def get_stt_object(stt_module="stub",
                   settings_tool: SettingsTool = None,
                   channels: Channels = None,
                   audio_recorder: AudioRecorder = None ):
    # get stt type. Current settings override the default
    stt_module = settings_tool.get_setting("stt_type") or stt_module

    # Import the selected Speech To Text module
    if stt_module == "stub":
        import core_utils.speech_to_text.stub_stt as STT
    elif stt_module == "google":
        import core_utils.speech_to_text.google_cloud_stt as STT
    elif stt_module == "deepspeech":
        import core_utils.speech_to_text.deepspeech_stt as STT
    else:
        raise ValueError("Invalid STT type")

    # return an instance of the selected Speech To Text module
    stt_settings_tool = settings_tool.get_sub_tool(stt_module)
    return STT.STT(settings_tool=stt_settings_tool,
                   channels=channels,
                   audio_recorder=audio_recorder)


if __name__ == "__main__":
    stt = get_stt_object()
    print(stt)