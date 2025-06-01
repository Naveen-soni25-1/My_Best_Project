from random import randint
import pygame

class Food:
    """A class to manage food for snake"""

    def __init__(self, s_game):
        """Initializing the food attributes"""
        self.screen = s_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = s_game.settings
        
        # Food settings
        self.color = self.settings.food_color
        self.radius = 8

        # Set initial position
        self._set_random_position()

    def _set_random_position(self):
        """Set a random position and define the rect for collision"""
        self.x = randint(self.radius + self.settings.wall_width,
                         self.screen_rect.width - self.radius - self.settings.wall_width)
        self.y = randint(self.radius + self.settings.wall_width,
                         self.screen_rect.height - self.radius - self.settings.wall_width)
        
        # Create a collision rect (square around the circle)
        self.rect = pygame.Rect(
            self.x - self.radius, self.y - self.radius,
            self.radius * 2, self.radius * 2
        )

    def draw_food(self):
        """A method to draw food on the screen"""
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    def relocate(self):
        """Relocate the food after being eaten"""
        self._set_random_position()
