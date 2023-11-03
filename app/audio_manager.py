import pygame

class AudioManager:
    def __init__(self):
        self.initialize_mixer()

    def initialize_mixer(self):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.5)  # Set default volume

    def play_audio(self, file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

    def stop_audio(self):
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)
