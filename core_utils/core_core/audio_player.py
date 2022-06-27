#########################################
# Audio Player
#########################################
from time import sleep
from pygame import mixer




class AudioPlayer:
    # base standard volume
    def __init__(self):
        mixer.init()
        volume = 1

        # voice
        self.voice_channel = mixer.Channel(0)


    def play(self, filename:str = None):
        mixer.music.load(filename)
        mixer.music.play()



    def pause(self):

        mixer.music.pause()



    def resume(self):
        mixer.music.unpause()



    def stop(self):
        mixer.music.stop()


    def play_sound(self, filename:str = None):
        newsound = mixer.Sound(filename)
        newsound.play()


    def stop_sound(self):
        mixer.Sound.stop()
        


# def audio_increase_volume():


##############
# Test
##############
if __name__ == "__main__":
    TEST_FILEPATH = "test assets/background.mp3"

    if TEST_FILEPATH:
        player = AudioPlayer()

        print("Test Music Player")
        print("Playing:", TEST_FILEPATH)
        player.play(filename=TEST_FILEPATH)
        sleep(4)
        print("Stopping")
        player.stop()

        print("Test Sound Player")
        print("Playing:", TEST_FILEPATH)
        player.play_sound(filename=TEST_FILEPATH)
        sleep(4)
        print("Stopping")
        player.stop_sound()


    else:
        print("No test filepath specified.")