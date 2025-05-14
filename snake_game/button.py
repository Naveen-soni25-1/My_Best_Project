import pygame.font

class Button:
    """A class to make button"""

    def __init__(self, s_game, msg, text_color=(255, 255, 255), position=None, bg_color=(0, 0, 0), size=36):
        """Initialize the button attributes."""
        self.screen = s_game.screen
        self.screen_rect = self.screen.get_rect()

        # set dimension of button its property
        self.button_width, self.button_height = 100, 50
        self.button_color = bg_color
        self.text_color = text_color
        self.text_size = size
        self.font = pygame.font.SysFont(None, self.text_size)

        # build rect button and prepare its position
        self.rect = pygame.Rect(0, 0, self.button_width, self.button_height)
        self.rect.center = self.screen_rect.center
        if position is not None:
            self.rect.x = position[0]
            self.rect.y = position[1]
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """ A method to write text in button."""
        self.text_image = self.font.render(msg, True, self.text_color)
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.center = self.rect.center
    
    def draw_button(self):
        """A class to draw button"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.text_image, self.text_image_rect)