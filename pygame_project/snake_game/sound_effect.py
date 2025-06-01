import pygame.mixer

class SoundEffect:
    """A class to maintain sound effect for game"""
    def __init__(self):
        """Initializing the sound attributes"""
        pygame.mixer.music.load("sounds/background_music.mp3")
        self.eat_sound = pygame.mixer.Sound("sounds/eating_sound.mp3")
        self.game_over_sound = pygame.mixer.Sound("sounds/game_over.mp3")


    def play_background_music(self):
        """play background music"""
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def stop_background_music(self):
        """stop the background music"""
        pygame.mixer.music.stop()
        
    def play_eat_sound(self):
        self.eat_sound.play()
        self.eat_sound.set_volume(1)
    
    def play_game_over_sound(self):
        """Play game over sound"""
        self.game_over_sound.play()
        self.game_over_sound.set_volume(1)