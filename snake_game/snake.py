import pygame
import math
from random import randint

class Snake:
    def __init__(self, s_game, settings):
        self.screen = s_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = settings
        self.segment_size = settings.snake_size
        self.stat = s_game.stats

        self.move_right = True
        self.move_left = False
        self.move_up = False
        self.move_down = False

        # Initial snake (self.head + 4 body segments)
        self.segments = []
        self.start_x, self.start_y = randint(100, 700), randint(100, 300)
        

        self.head_position = []
        for i in range(10):
            rect = pygame.Rect(self.start_x - i * self.segment_size +30, self.start_y, self.segment_size, self.segment_size)
            self.segments.append(rect)

    def update_snake(self):
        """update snake movemnet"""
        self.speed = self.stat.snake_speed
        self.max_history = len(self.segments) * self.segment_size

        # Move the self.head
        self.head = self.segments[0]
        if self.move_right and self.head.right < self.screen_rect.right - self.settings.wall_width:
            self.head.x += self.speed
            self.angle = 0
        elif self.move_left and self.head.left > self.screen_rect.left + self.settings.wall_width:
            self.head.x -= self.speed
            self.angle = 180
        elif self.move_up and self.head.top > self.screen_rect.top + self.settings.wall_width:
            self.head.y -= self.speed
            self.angle = 90
        elif self.move_down and self.head.bottom < self.screen_rect.bottom - self.settings.wall_width:
            self.head.y += self.speed
            self.angle = 270
 
        self.head_position.insert(0, (self.head.x, self.head.y))
        if len(self.head_position) > self.max_history:
            self.head_position.pop()

        

# Smooth, speed-based spacing using logarithmic decay
        if self.speed <= 6:
            self.spacing = max(1, int(6 - self.speed / 2))
        else:
        # Logarithmic scaling: prevents spacing from jumping suddenly
            self.spacing = max(1, int(2 + math.log(self.speed - 5, 1.5)))

        for i in range(1, len(self.segments)):
            pos_index = i * self.spacing
            if pos_index + 1 < len(self.head_position):
                x1, y1= self.head_position[pos_index]
                x2, y2 = self.head_position[pos_index + 1]
                self.segments[i].x = (x1 + x2)//2
                self.segments[i].y = (y1 + y2)//2

    def draw_snake(self):
        for i, rect in enumerate(self.segments):
            color = self.settings.snake_color if i == 0 else (191, 180, 220)
            pygame.draw.rect(self.screen, color, rect, border_radius=8,)

    def grow(self):
        # Add new segment at the last segment’s position
        tail = self.segments[-1]
        for _ in range(2):
            new_rect = pygame.Rect(tail.x, tail.y, self.segment_size, self.segment_size)
            self.segments.append(new_rect)

    def rest_snake(self):
        """reset snake position"""
        self.start_x, self.start_y = randint(100, 700), randint(100, 300)
        self.segments.clear()
        for i in range(10):
            rect = pygame.Rect(self.start_x - i * self.segment_size + 30, self.start_y, self.segment_size, self.segment_size)
            self.segments.append(rect)
        self.head_position.clear()
