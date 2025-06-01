from pygame.font import Font

class ScoreBoard:
    """A class to report scoring information"""
    
    def __init__(self, s_game):
        """initialize the score board"""
        self.screen = s_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = s_game.settings
        self.stats = s_game.stats
        self.bg_color = (0, 0, 0)
    
        self.font = Font(None, self.settings.font_size)

        # prepare the initial image
        self.prep_score()
        self.prep_high_score()
 
    def prep_score(self):
        """turn the score into a rendered image"""
        score_str = f"{self.settings.score_text} {self.stats.score}"
        self.score_image = self.font.render(score_str, True, self.settings.score_text_color, self.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.topleft = self.screen_rect.topleft

    def prep_high_score(self):
        """turn the high score into a render image"""
        hight_score_str = f"{self.settings.high_score_text} {self.stats.high_score}"
        self.high_score_image = self.font.render(hight_score_str, True, self.settings.high_score_color, self.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.midtop = self.screen_rect.midtop

    def check_high_score(self):
        """check high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """draw scores on screen"""
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.score_image, self.score_rect)