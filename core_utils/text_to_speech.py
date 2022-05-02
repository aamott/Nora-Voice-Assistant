# For loading keys and data
import json

# For working with audio
from playsound import playsound
import speech_recognition as sr
from os import remove

# Temporary fix for playsound is to specify the entire filepath like so:
# path.abspath(filename).replace("\\", "/")
from os import path




#######################################
# IBM Text to Speech - Requires an API key
#######################################
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    
class IBM_TTS:
    # The id of the object as it will appear in the json
    id = "IBM_TTS"
    voices = ["en-US_EmilyV3Voice", "en-US_AllisonVoice", "en-US_HenryV3Voice", "en-AU_CraigVoice"]

    def __init__(self, api_key, service_url, voice = 'en-US_AllisonVoice'):
        """ IBM's Text to Speech wrapper for Alfred

            Parameters:
                key: key obtained from an IBM developer account
                service_url: Service URL from the same IBM developer account
                voice: The voice to be used
        """
        self.voice = voice
        authenticator = IAMAuthenticator(api_key)
        self.text_to_speech = TextToSpeechV1(
            authenticator=authenticator
        )

        self.text_to_speech.set_service_url(service_url)
            
    def say(self, text):
        filename = "tts.mp3"
        with open(filename,'wb') as audio_file:
            audio_data = self.text_to_speech.synthesize(text,voice=self.voice,accept='audio/mp3').get_result().content
            audio_file.write(audio_data)
        
        playsound(path.abspath(filename).replace("\\", "/"))
        remove(filename)
            
######################################
# Google Text to Speech
#
######################################
from gtts import gTTS
class Google_TTS:
    # The id of the object as it will appear in the json
    id="Google_TTS"

    def __init__(self, ):
        pass
        
    def say(self, text):
        # send audio to google and save it as a file
        filename = "tts.mp3"
        google_audio = gTTS(text)
        google_audio.save(filename)

        # play speech then remove the file
        playsound(path.abspath(filename).replace("\\", "/"))
        remove(filename)

###########################################
# Microsoft Text to Speech
# Documentation:
#    https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-text-to-speech?tabs=script%2Cbrowserjs%2Cwindowsinstall&pivots=programming-language-python
# For a list of voices, please visit
#    https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#prebuilt-neural-voices
# Requirements
#    pip install azure-cognitiveservices-speech
###########################################
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import AudioOutputConfig # for audio output
class MS_Voice:
    # The id of the object as it will appear in the json
    id = "MS_Voice"

    def __init__(self, api_key, location_region, voice_name = "en-IE-EmilyNeural", language = None):
        """ Microsoft's Text to Speech wrapper for Alfred
            Find your key and resource region under the 'Keys and Endpoint' tab in your Speech resource in Azure Portal

            Parameters:
                api_key: key obtained from a developer account
                location_region: Location Region associated with the key (ex. "usgovarizona", "westus")
                voice_name: Name of voice
        """
        self.speech_config = speechsdk.SpeechConfig(subscription=api_key, region=location_region)
        if voice_name: 
            self.speech_config.speech_synthesis_voice_name = voice_name
        if language:
            self.speech_config.speech_synthesis_language = language # For example, "de-DE"
            
        #specific to listening
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config)

    def say(self, text, synthesize_to_file = False, filename="synthesized_speech.wav", synthesize_to_stream = False, is_ssml = False):
        #In this sample we are using the default speaker 
        #Learn how to customize your speaker using SSML in Azure Cognitive Services Speech documentation
        if synthesize_to_file:
            audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)
        elif synthesize_to_stream: # Return the pure audio stream as a bytes object
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=None)
            result = synthesizer.speak_text_async(text).get()
            stream = AudioDataStream(result)
            return stream # a bytes object
        else:
            audio_config = AudioOutputConfig(use_default_speaker=True)
            
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=audio_config)
        
        if is_ssml:
            synthesizer.speak_ssml_async(text)
        else:
            synthesizer.speak_text_async(text)
        
    def listen(self):
        
        #Asks user for mic input and prints transcription result on screen
        print("Listening...")
        result = self.speech_recognizer.recognize_once_async().get()
        print(result.text)
        
        return result.text