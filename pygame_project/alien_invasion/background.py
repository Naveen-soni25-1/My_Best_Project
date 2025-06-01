import pygame

class Background:
    """A class to manage the background."""

    def __init__(self, ai_game, image_path, image_size=(1400, 700), position=(0,0)):
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.smoothscale(self.image, (image_size))
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self, position):
        """update the bacground position."""
        self.x = position[0]
        self.y = position[1]

        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)