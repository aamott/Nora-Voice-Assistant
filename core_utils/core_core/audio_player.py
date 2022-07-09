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

        self.sounds = []


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
        """Play Sound
        :param filename (str): filename of wave file or buffer object
        :return: pygame.mixer.Sound
        """
        newsound = mixer.Sound(filename)
        newsound.play()
        self.sounds.append(newsound)
        return newsound


    def stop_sound(self):
        """Stop all playing sounds
             Does not stop music.
        """
        for sound in self.sounds:
            sound.stop()



# def audio_increase_volume():


##############
# Test
##############
if __name__ == "__main__":
    MP3_FILEPATH = "test assets/background.mp3"
    WAV_FILEPATH1 = "test assets/batman_theme_x.wav"
    WAV_FILEPATH2 = "test assets/batman_music_sfx.wav"

    if MP3_FILEPATH:
        player = AudioPlayer()

        print("Test Sound Player")
        print("Playing:", WAV_FILEPATH1)
        player.play_sound(filename=WAV_FILEPATH1)
        sleep(3)

        print("Test Sound Player")
        print("Playing:", WAV_FILEPATH2)
        player.play_sound(filename=WAV_FILEPATH2)
        sleep(4)
        print("Stopping")
        player.stop_sound()

        print("Test Music Player")
        print("Playing:", MP3_FILEPATH)
        player.play(filename=MP3_FILEPATH)
        sleep(4)
        print("Stopping")
        player.stop()


    else:
        print("No test filepath specified.")