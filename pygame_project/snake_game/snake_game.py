import sys 
from time import sleep

import pygame

from background import Background
from background import wall
from food import Food
from game_stats import GameStats
from scoreboard import ScoreBoard
from settings import Settings
from snake import Snake
from sound_effect import SoundEffect
from starting_menu import StartMenu
from game_over import GameOver

class SnakeGame:
    """A class to manage snake game and its resources"""

    def __init__(self):
        """Initialize the game attributes"""
        pygame.init()
        self.settings = Settings(self)
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Snake Game")

        self.wall = wall(self, self.settings)
        self.bg_image = Background(self, "images/background.jpg")
        self.food = Food(self)
        self.sound_effect = SoundEffect()
        self.menu = StartMenu(self)
        self.stats = GameStats(self)
        self.scoreboard = ScoreBoard(self)
        self.snake = Snake(self, self.settings)
        self.clock = pygame.time.Clock()
        self.game_over = GameOver(self)

        self.play_game = False
        self.menu_mode = True
        self.game_over_flag = False

        if self.play_game:
            self.sound_effect.play_background_music()
        if self.game_over_flag:
            pygame.mouse.set_visible(True)

    def run_game(self):
        """Run the main game loop"""
        while True:
            self._check_events()
            if self.play_game:
                self.snake.update_snake()
                self.food.draw_food()
                self._check_food_snake_collision()           
                self._check_wall_snake_collision()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)   
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.menu_mode:
                    self._check_menu_mode(mouse_pos)
                if self.game_over_flag:
                    self._check_game_over_mode(mouse_pos)

    def _check_menu_mode(self, mouse_pos):
        """a method to check mouse button collision."""
        play_button_clicked = self.menu.play_button.rect.collidepoint(mouse_pos)
        quit_button_clicked = self.menu.quit_button.rect.collidepoint(mouse_pos)

        if play_button_clicked and not self.play_game:
            self.play_game = True
            pygame.time.delay(100)
            self.menu_mode = False
            self.game_over_flag = False
            pygame.mouse.set_visible(False)
            self.stats.reset_game()
            self.snake.rest_snake()
            pygame.display.update()
            
        elif quit_button_clicked and not self.play_game:
            sys.exit()

    def _check_game_over_mode(self, mouse_pos):
        """a helping mwthod to check game over"""
        play_again_button_clicked = self.game_over.play_again.rect.collidepoint(mouse_pos)
        quit_button_clicked = self.game_over.quit_button.rect.collidepoint(mouse_pos)

        if play_again_button_clicked and not self.play_game:
            self.stats.reset_game()
            self.game_over_flag = False
            self.menu_mode = True
            pygame.mouse.set_visible(True)
            
        elif quit_button_clicked and not self.play_game:
            sys.exit()
            
    def _check_keydown_events(self, events):
        """check keypresses and respond to it."""
        if events.key == pygame.K_q:
            sys.exit()
        elif events.key == pygame.K_p:
           self._start_game()

        elif events.key == pygame.K_BACKSPACE:
            self._pause_game()

        elif events.key == pygame.K_RIGHT and not self.snake.move_left:
            self.snake.move_right = True
            self.snake.move_left = self.snake.move_up = self.snake.move_down = False

        elif events.key == pygame.K_LEFT and not self.snake.move_right:
            self.snake.move_left = True
            self.snake.move_right = self.snake.move_up = self.snake.move_down = False

        elif events.key == pygame.K_UP and not self.snake.move_down:
            self.snake.move_up = True
            self.snake.move_left = self.snake.move_right = self.snake.move_down = False

        elif events.key == pygame.K_DOWN and not self.snake.move_up:
            self.snake.move_down = True 
            self.snake.move_left = self.snake.move_up = self.snake.move_right = False

    def _check_wall_snake_collision(self):
        """Check collision between snake and wall"""
        head = self.snake.segments[0]
        for wall_rect in self.wall.rects:
            if head.colliderect(wall_rect):
                self.play_game = False
                self.menu_mode = False
                self.game_over_flag = True
                break

    def _check_food_snake_collision(self):
        """Check collision between snake and food"""
        self.head = self.snake.segments[0]
        if self.head.colliderect(self.food.rect):
            self.food.relocate()
            self.snake.grow()
            self.stats.score += 1
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()
            self.sound_effect.play_eat_sound()

        if int(self.stats.score) % 7 == 0 and self.stats.score != self.stats.last_speedup_score:
            if self.stats.snake_speed < 12:
                self.stats.snake_speed += 0.2
                self.stats.last_speedup_score = self.stats.score

    def _start_game(self):
        """start game and reset game"""        
        if self.menu_mode:
            self.play_game = True
            pygame.time.delay(500)
            self.menu_mode = False
            pygame.mouse.set_visible(False)
            self.stats.reset_game()
            self.snake.rest_snake()

    def _pause_game(self):
        """reset the game"""
        if self.play_game:
            self.play_game = False
            self.menu_mode = True
            pygame.mouse.set_visible(True)
        
    def _update_screen(self):
        """Update screen with all the changes"""
        self.screen.fill(self.settings.bg_color)
        self.scoreboard.show_score()

        if self.play_game:
            self.bg_image.blit_bg_image()
            self.snake.draw_snake()
            self.food.draw_food()
            self.wall.draw_wall()

        elif self.game_over_flag and not self.play_game:
            self.game_over.call_draw_button()
            self.sound_effect.play_game_over_sound()
            self.sound_effect.stop_background_music()

        elif self.menu_mode:
            self.menu.call_draw_button()   
    
        pygame.display.flip()
        self.clock.tick(60)

if __name__ == '__main__':
    sn = SnakeGame()
    sn.run_game()
