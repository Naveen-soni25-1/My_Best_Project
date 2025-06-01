class Setting:
    """A class to Maintain game setttings."""

    def __init__(self):
        """Initialize the settings attributes"""
        self.game_name = "Space Dodge Game"
        self.screen_width = 1000
        self.screen_height = 600

        # game stats
        self.score = 0
        self.treasure_speed = 1
        self.ship_speed = 10