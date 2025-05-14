from button import Button
import pygame

class GameOver:
    """A class to represent starting menu"""
    
    def __init__(self, s_game):
        """Initialize the game attribute"""
        self.screen = s_game.screen
        self.settings = s_game.settings
        self.screen_rect = self.screen.get_rect()
        self.bg_color = (0, 0, 0)
        self.game_over_button = Button(self, "Game Over", (255, 255, 255), None, self.bg_color, 80)
        self.quit_button = Button(self, "Quit", (255, 255, 255), (0, 20), self.bg_color, 40)
        self.play_again = Button(self, "Play Again", (255, 255, 255), (860, 20), self.bg_color, 40)
        self.call_draw_button()

    def call_draw_button(self):
        """A method to draw button screen"""
        self.screen.fill((0, 0, 0))
        pygame.mouse.set_visible(True)
        self.game_over_button.draw_button()
        self.quit_button.draw_button()
        self.play_again.draw_button()