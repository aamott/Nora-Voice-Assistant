from pygame import mixer




#########################################
# basic audio oupt and commands
# play, pause, resume, and etc
#########################################





class AudioPlayer:
# base standard volume 
    def __init__():
        mixer.init()
        volume = 1


    def play(self, filename:str = None, audio_data:ndarray = None):
        mixer.music.load()
        mixer.music.play()



    def pause():

        mixer.music.pause()  



    def resume():
        mixer.music.unpause()



    def stop():
        mixer.music.stop()


    def play_sound(self, filename:str = None, audio_data:ndarray = None):
        mixer.Sound.load()
        mixer.Sound.play()

    def stop_sound(self):
        mixer.Sound.stop()



# def audio_increase_volume():
