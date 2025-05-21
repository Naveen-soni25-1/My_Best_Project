from pygame.font import Font

class ScoreBoard:
    """A class to manage score board."""
    
    def __init__(self, game):
        """Iitialize the score board attributes."""
        self.game = game
        self.screen = self.game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = self.game.settings
        self.font = Font(None, 24)
        self.prep_score()
        self.prep_high_score()
        
    def prep_score(self):
        """Prepare the score image."""
        self.score_str = f"Score: {str(self.game.stats.score)}"
        self.score_image = self.font.render(self.score_str, True, (255, 255, 255))
        self.score_rect = self.score_image.get_rect()
        self.score_rect.topright = self.screen_rect.topright
        self.score_rect.x -= 10
        self.score_rect.y += 10
    
    def prep_high_score(self):
        """Prepare the high score image."""
        self.high_score_str = f"High Score: {str(self.game.stats.high_score)}"
        self.high_score_image = self.font.render(self.high_score_str, True, (255, 255, 255))
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.midtop = self.screen_rect.midtop
        self.high_score_rect.y += 10

    def check_high_score(self):
        """A method to check high score and update."""
        if self.game.stats.score > self.game.stats.high_score:
            self.game.stats.high_score = self.game.stats.score
            self.prep_high_score()

    def draw_score(self):
        """A Method to draw score on screen"""
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.score_image, self.score_rect)