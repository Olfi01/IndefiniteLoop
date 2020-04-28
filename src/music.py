"""In this file the methods for playing music and sounds are being collected."""
import pygame
from game_data import GameData
from pygame.mixer import Sound


class SoundManager:
    """A class to manage playing sounds, which keeps its own access to the game data."""
    def __init__(self, game_data):
        """Initializes a new Sound Manager with the given access to the game data.
        :type game_data: GameData"""
        self.game_data = game_data

    def play_music(self):
        """Starts to infinitely loop the currently loaded music from the beginning."""
        if not self.game_data.is_music_on():
            return
        pygame.mixer.music.rewind()
        pygame.mixer.music.play(-1)

    def play_sound(self, sound):
        """Plays a sound if the sounds aren't muted.
        :type sound: Sound"""
        if not self.game_data.is_sound_on():
            return
        sound.play()


def load_music(path):
    """Loads the background music from the given path.
    :type path: str"""
    pygame.mixer.music.load(path)


def stop_music():
    """Stops the currently playing background music."""
    pygame.mixer.music.fadeout(100)
