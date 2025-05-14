import pygame

class wall:
    def __init__(self, s_game, settings):
        self.screen = s_game.screen
        self.setting = settings
        self.screen_rect = self.screen.get_rect()

        # Create 4 wall rectangles
        w = self.setting.wall_width
        sr = self.screen_rect

        self.rects = [
            pygame.Rect(sr.left, sr.top, sr.width, w),            # Top wall
            pygame.Rect(sr.left, sr.bottom - w, sr.width, w),     # Bottom wall
            pygame.Rect(sr.left, sr.top, w, sr.height),           # Left wall
            pygame.Rect(sr.right - w, sr.top, w, sr.height)       # Right wall
        ]

    def draw_wall(self):
        for rect in self.rects:
            pygame.draw.rect(self.screen, self.setting.wall_color, rect)
  

class Background:
    """a class to draw background"""
    def __init__(self, s_game, path=None):
        """initialize the screen background image"""
        self.screen = s_game.screen
        self.setting = s_game.settings
        self.screen_rect = self.screen.get_rect()
        self.bg_image = pygame.image.load(path)
        self.bg_image = pygame.transform.scale(self.bg_image, (1000, 500))
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.midbottom = self.screen_rect.midbottom
    
        
    def blit_bg_image(self):
        """Blit the background image."""
        self.screen.blit(self.bg_image, self.bg_rect)