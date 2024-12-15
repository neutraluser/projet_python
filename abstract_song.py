from abc import ABC, abstractmethod
import pygame

class MusicHandler(ABC):

    def __init__(self, track):
        self.track = track

    @abstractmethod
    def load_music(self):
        pass

    @abstractmethod
    def play_music(self):

        pass

    @abstractmethod
    def stop_music(self):

        pass


class PygameMusicHandler(MusicHandler):
    """
    Implémentation de MusicHandler utilisant pygame.
    """

    def load_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.track)

    def play_music(self):
        pygame.mixer.music.play(-1)  # Lecture en boucle

    def stop_music(self):
        pygame.mixer.music.stop()
