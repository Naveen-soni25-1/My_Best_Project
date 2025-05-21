import pygame

class Instruction:
    """A class to create starting menu for game."""

    def __init__(self, game):
        """Initializing the class attributes."""
        self.game = game
        self.screen = self.game.screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load(r"images\instruction.png")
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

    def draw(self):
        """A method to draw start menu."""
        self.screen.blit(self.image, self.rect)