#########################################
# Audio Player
#########################################
from time import sleep
from pygame import mixer
import wave
import numpy as np



class AudioPlayer:
    # base standard volume
    def __init__(self):
        mixer.init()
        volume = 1


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
        mixer.Sound.load(filename)
        mixer.Sound.play()

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
        player.play(filename=TEST_FILEPATH)
        sleep(10)
        player.stop()

    else:
        print("No test filepath specified.")