class GameStats:
    """Track statistics for alien invasion"""

    def __init__(self,ai_game):
        """initialize statics""" 
        self.settings = ai_game.settings
        self.ai_game = ai_game
        self.high_score = 0
        self.reset_stats()

    def reset_stats(self):
        """initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
    
    def reset_game(self):
        """go back to the initial menu of the game"""
        self.ai_game.aliens.empty()
        self.ai_game.bullets.empty()
        self.ai_game.ship.center_ship()
        self.reset_stats()