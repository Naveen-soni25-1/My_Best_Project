from random import randint

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0) # black

        # Ship settings
        self.ship_limit = 3
        
        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 183, 250)
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        # upscale the game
        self.upscale_speed = 1.2
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        """initialize the initial game speed"""
        self.ship_speed = 4
        self.bullet_speed = 4
        self.alien_speed = 1.0
        self.alien_points = 15
        self.fleet_drop_speed = 10

    def increase_speed(self):
        """speed up the game"""
        self.ship_speed *= self.upscale_speed
        self.bullet_speed *= self.upscale_speed
        self.alien_speed *= self.upscale_speed
        self.alien_points = int(self.alien_points * self.score_scale)

    def mode_settings(self, mode):
        """respond to the mode select by the player"""
        if mode == "relax":
            self.ship_speed = 2
            self.bullet_speed = 2
            self.alien_speed = 0.5
            self.alien_points = 10
        elif mode == "Chill":
            self.ship_speed = 4
            self.bullet_speed = 4
            self.alien_speed = 1.0
            self.alien_points = 15
        elif mode == "Insane":
            self.ship_speed = 8
            self.bullet_speed = 8
            self.alien_speed = 4
            self.alien_points = 30
            self.fleet_drop_speed = 30