import pygame
import random

class Treasure(pygame.sprite.Sprite):
    def __init__(self, game, image_path):
        super().__init__()
        self.game = game
        self.screen = self.game.world
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()

        # Random position in the world
        self.relocate()
        self.rect.center = self.pos

        # Random drifting velocity
        angle = random.uniform(0, 360)
        speed = self.game.stats.treasure_speed
        self.velocity = pygame.Vector2(speed, 0).rotate(angle)

        # For optional spinning
        self.rotation = 0
        self.rotation_speed = random.uniform(-1, 1)  # degrees per frame

    def relocate(self):
        """A method to change position"""
        self.pos = pygame.Vector2(random.randint(0, 4500), random.randint(0, 4500))

    def update(self):
        # Move
        self.pos += self.velocity
        self.rect.center = self.pos

        # Rotate (optional)
        self.rotation += self.rotation_speed
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.edge_bounce()

    def edge_bounce(self):
        """A method to bounce the obstacle off the edge of the world."""
        if self.rect.left < 0 or self.rect.right > self.game.world.get_width():
            self.velocity.x *= -1
        if self.rect.top < 0 or self.rect.bottom > self.game.world.get_height():
            self.velocity.y *= -1
        self.pos += self.velocity
        self.rect.center = self.pos
        self.rotation += self.rotation_speed
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)

    def blit_treasure(self):
        self.screen.blit(self.original_image, self.rect)