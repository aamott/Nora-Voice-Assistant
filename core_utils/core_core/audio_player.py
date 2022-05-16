from pygame import mixer




#########################################
# basic audio oupt and commands
# play, pause, resume, and etc
#########################################


mixer.init()


class AudioPlayer:
# base standard volume 
    volume = 1


    def play_audio(x):
        mixer.Sound.load(x)
        mixer.Sound.play(x)



    def audio_pause():

        mixer.Sound.pause()  



    def audio_resume():
        mixer.Sound.unpause()



    def audio_stop():
        mixer.Sound.stop()



# def audio_increase_volume():
