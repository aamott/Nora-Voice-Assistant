from pygame import mixer
import wave
import numpy as np




#########################################
# basic audio oupt and commands
# play, pause, resume, and etc
#########################################





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
