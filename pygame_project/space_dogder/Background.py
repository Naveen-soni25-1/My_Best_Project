import pygame

class Background:
    """A class to draw background."""

    def __init__(self, bg_location, path ,size=None, position=None):
        """Initializing the background attributes."""
        self.screen = bg_location.world
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load(path).convert_alpha()
        if size:
            self.image = pygame.transform.smoothscale(self.image, size) 
            
        self.image_rect = self.image.get_rect()
        if position:
            self.update_bg(position)
        else:
            self.image_rect.midbottom = self.screen_rect.midbottom
    
    def update_bg(self, position):
        """Update the bg position."""
        self.image_rect.topleft = position

    def draw_bg_image(self):
        """A method to draw image on screen."""
        self.screen.blit(self.image, self.image_rect)