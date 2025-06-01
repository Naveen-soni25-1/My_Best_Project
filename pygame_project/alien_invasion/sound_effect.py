import pygame.mixer

class SoundEffect:
    """A class to manage sound effects."""
    
    def __init__(self, ai_game):
        """Initialize the sound effects."""
        self.settings = ai_game.settings
        pygame.mixer.init() 
        pygame.mixer.music.load('sounds/background_music.mp3')
        pygame.mixer.music.set_volume(0.5)
        self.game_over_sound = pygame.mixer.Sound("sounds/game_over.mp3")
        self.game_over_sound.set_volume(1)
    
        self.bullet_sound = pygame.mixer.Sound("sounds/laser_bullet.mp3")
        self.explosion_sound = pygame.mixer.Sound("sounds/explosion.mp3")
        


    def play_background_music(self):
        """play the background music"""
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
    
    def stop_background_music(self):
        """stop the background music"""
        pygame.mixer.music.stop()
    
    def play_bullet_sound(self):
        """play the sound effect for shooting a bullet"""
        self.bullet_sound.play()
        self.bullet_sound.set_volume(2.0)
        self.bullet_sound.play(0, 0, 0)

    def play_explosion_sound(self):
        """play the sound effect of explosion"""
        self.explosion_sound.play()
        self.explosion_sound.set_volume(1)
        self.explosion_sound.play(0, 0, 0)

    def play_game_over_sound(self):
        """play the sound effect of game_over"""
        self.game_over_sound.play(0, 0 , 0)
    def stop_game_over_sound(self):
        """stop the sound effect of the game_over"""
        self.game_over_sound.stop()