from settings import Setting

class GameStat:
    """A class to manage game score."""

    def __init__(self):
        """Initialize the class attributes."""
        self.settings = Setting()
        self.score = self.settings.score
        self.high_score = 0
        self.treasure_speed = self.settings.treasure_speed
        self.ship_speed = 30

    def reset_game(self):
        """A method to reset the game."""
        self.score = self.settings.score
        self.treasure_speed = self.settings.treasure_speed
        self.ship_speed = self.settings.ship_speed