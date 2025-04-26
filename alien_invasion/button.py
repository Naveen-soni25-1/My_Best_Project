import pygame.font 

class Button:
    """ A class to builf button on the screen"""
    def __init__(self, ai_game, msg, position=None, size=None, text_color=(0, 0, 0), bg_color=(65, 237, 199)):
        """initialize the game attributes"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # set the dimension of button and its properties
        self.width, self.height = 150, 50
        self.button_color = bg_color
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, size)

        # build the button rect and set its position
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center 
        self.y = float(self.rect.y)

        # prepare message for button
        self._prep_msg(msg)
        self.update_button(position)

    def _prep_msg(self, msg):
        """turn message into a render image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color) # text, antialise, text_color, beckground_color
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center # set the center of the text image to the center of the button


    def update_button(self, position=None):
        """update the position of button"""
        if position is not None:
            self.y += position
            self.rect.y = self.y
            self.msg_image_rect.centery = self.rect.centery

    def draw_button(self):
        """Draw the button on the screen"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)