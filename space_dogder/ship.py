import math
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage ship."""

    def __init__(self, sd_game):
        """Initialize the class attributes."""
        super().__init__()
        self.sd_game = sd_game
        self.world = self.sd_game.world
        self.world_rect = self.world.get_rect()

        self.original_image = pygame.image.load(r"images\ship.png")
        self.image = pygame.transform.smoothscale(self.original_image, (50, 70))
        self.rect = self.image.get_rect()
        self.rect.center = self.world_rect.center

        self.pos = pygame.math.Vector2(self.rect.center) # give ship position
        self.velocity = pygame.math.Vector2(0, 0) # 2D direction and speed (x and y)
        self.speed = self.sd_game.stats.ship_speed
        self.angle = 0

    def update_ship(self, keys):
        """A method to control ship movement."""
        self.velocity = pygame.math.Vector2(0, 0) # reset velocity 

        if keys[pygame.K_RIGHT]:
            self.velocity.x = 1
        if  keys[pygame.K_LEFT]:
            self.velocity.x = -1
        if keys[pygame.K_UP]:
            self.velocity.y = -1
        if keys[pygame.K_DOWN]:
            self.velocity.y = 1
        
        if self.velocity.length() > 0: # for speed
            self.velocity = self.velocity.normalize() * self.speed
            # velocity = unit vector(1) * speed scaler
            self.angle = self.velocity.angle_to(pygame.Vector2(0, -1))  # Up is 0° 
            # angle_to -> Returns the angle in degrees between two vectors (up and direction).
            self.rotate_ship()

        self.pos += self.velocity # move the object
        self.rect.center = self.pos

        self.pos.x = max(0, min(self.pos.x, self.world_rect.width ))
        self.pos.y = max(0, min(self.pos.y, self.world_rect.height))

    
    def rotate_ship(self):
        """A method to rotate the image"""
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.image = pygame.transform.smoothscale(self.image, (50, 70))
        self.rect = self.image.get_rect(center=self.rect.center)

    def reset(self):
        """A method to reset the shipS."""
        self.rect.center = self.world_rect.center
        self.pos = pygame.math.Vector2(self.rect.center)

    def blitme(self):
        """A method to draw ship."""
        self.world.blit(self.image, self.rect)