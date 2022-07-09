###########################################
# Microsoft Text to Speech and Text to Speech
# Documentation:
#    https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-text-to-speech?tabs=script%2Cbrowserjs%2Cwindowsinstall&pivots=programming-language-python
# For a list of voices, please visit
#    https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#prebuilt-neural-voices
# Requirements
#    pip install azure-cognitiveservices-speech
###########################################
from os import remove
from core_utils.text_to_speech.tts_abstract import TTS as TTS_Abstract
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool  # for audio output
from core_utils.core_core.audio_player import AudioPlayer
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream


class TTS(TTS_Abstract):
    # The id of the object as it will appear in the json
    name = "MS_Voice_TTS"

    def __init__(self, settings_tool: SettingsTool, channels: Channels, audio_player: AudioPlayer):
        """ Microsoft's Text to Speech wrapper for Alfred
            Find your key and resource region under the 'Keys and Endpoint' tab in your Speech resource in Azure Portal

            Parameters:
                api_key: key obtained from a developer account
                location_region: Location Region associated with the key (ex. "usgovarizona", "westus")
                voice_name: Name of voice
        """
        self.settings_tool = settings_tool
        self.channels = channels
        self.audio_player = audio_player

        # Add any settings that don't exist yet
        self.populate_settings_tool()
        self.settings_tool.save_settings()

        # Get settings
        api_key = self.settings_tool.get_setting("key")
        region = self.settings_tool.get_setting("region")
        voice = self.settings_tool.get_setting("voice")
        language = self.settings_tool.get_setting("language")

        self.speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)

        if not api_key:
            raise Exception("Please set the key in the settings")
        elif not region:
            raise Exception("Please set the region in the settings")

        if voice:
            self.speech_config.speech_synthesis_voice_name = voice
        if language:
            self.speech_config.speech_synthesis_language = language # For example, "de-DE"

        #specific to listening
        # self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config)


    def say(self, text, is_ssml=False):
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=None)
        speech_synthesis_result = synthesizer.speak_text_async(text).get()
        # # TODO: Figure out how to use the bytes object without it playing super fast
        # Bytes object:
        # self.audio_player.play(speech_synthesis_result.audio_data)

        # Save to wav to be played
        stream = AudioDataStream(speech_synthesis_result)
        stream.save_to_wav_file_async("tts.wav").get()
        self.audio_player.play_sound('tts.wav')
        remove('tts.wav')


        # The code used before the AudioUtils.play_speech was implemented
        # audio_config = AudioOutputConfig(use_default_speaker=True)
        # synthesizer = speechsdk.SpeechSynthesizer(
        #     speech_config=self.speech_config, audio_config=audio_config)
        # # Speak the result
        # if is_ssml:
        #     speech_synthesis_result = synthesizer.speak_ssml_async(text).get()
        # else:
        #     speech_synthesis_result = synthesizer.speak_text_async(text).get()

        # Debugging
        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(
                        cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")

        return speech_synthesis_result.audio_data


    def populate_settings_tool(self):
        """ Populates the settings tool with the settings for this TTS object. 
            Does not overwrite existing settings. """
        if not self.settings_tool.get_setting("key"):
            self.settings_tool.set_setting("key", None)
        if not self.settings_tool.get_setting("region"):
            self.settings_tool.set_setting("region", None)
        if not self.settings_tool.get_setting("voice"):
            self.settings_tool.set_setting("voice", None)
        if not self.settings_tool.get_setting("language"):
            self.settings_tool.set_setting("language", None)


if __name__ == "__main__":
    tts = TTS()
    tts.say("Hello World")