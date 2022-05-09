#######################################
# Google Cloud Speech
# Requires:
#     pip install google-cloud-speech
#######################################
from google.cloud import speech


class Google_STT:
    # The id of the object as it will appear in the json
    name = "Google_STT"

    def __init__(self, credentials_file='credentials.json'):
        self.client = speech.SpeechClient.from_service_account_json(
            credentials_file)

    def listen(self):
        """
        Listens for audio, then returns the text of the audio
        """
        # record
        with self.mic as source:
            audioData = self.sr.listen(source)
