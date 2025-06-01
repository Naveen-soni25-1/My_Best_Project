from snake import Snake
from random import randint

class GameStats:
    """A class to managage game resources"""

    def __init__(self, s_game):
        """initialize the game statistic"""
        self.s_game = s_game
        self.settings = s_game.settings
        self.snake_speed = s_game.settings.snake_speed
        self.score = 0
        self.high_score = 0
        self.snake_size = self.settings.snake_speed
        self.last_speedup_score = 0
        self.reset_game()

    def reset_game(self):
        """reset the game state"""        
        self.score = self.settings.score
        self.high_score = self.settings.high_score
        self.snake_speed = self.settings.snake_speed
        self.snake_size = self.settings.snake_size
        self.last_speedup_score = 0