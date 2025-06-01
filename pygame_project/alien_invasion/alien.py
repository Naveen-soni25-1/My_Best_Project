import pygame
from pygame.sprite import Sprite

# A sprite is just an object in your game that can move, be drawn, and interact with other objects.
class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen # get the screen from the ai_game instance.
        self.settings = ai_game.settings # get the settings from the ai_game instance.

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/alien.png')
        self.image = pygame.transform.smoothscale(self.image, (75, 65))
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width  # set the x position of the alien
        self.rect.y = self.rect.height # set the y position of the alien

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)
    
    def check_edges(self):
        """Return true if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0) # return true or false
    
    def update(self):
        """move the alien to the right."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction 
        self.rect.x = self.x 