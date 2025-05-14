from button import Button
from background import Background

class StartMenu:
    """A class to represent starting menu"""
    
    def __init__(self, s_game):
        """Initialize the game attribute"""
        self.screen = s_game.screen
        self.settings = s_game.settings
        self.screen_rect = self.screen.get_rect()
        self.bg_color = (0, 0, 0)
        self.play_button = Button(self, "Play", (255, 255, 255), None, (32, 31, 45), 50)
        self.quit_button = Button(self, "Quit", (255, 255, 255), (0, 20), (15, 14, 18), 40)
        self.menu_bg = Background(self, "images/menu_background.jpg")
        
        self.call_draw_button()

    def call_draw_button(self):
        """A method to draw button screen"""
        self.menu_bg.blit_bg_image()
        self.play_button.draw_button()
        self.quit_button.draw_button()