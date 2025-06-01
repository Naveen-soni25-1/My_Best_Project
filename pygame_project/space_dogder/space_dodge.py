import sys
import json

import pygame
from time import sleep

from settings import Setting
from Background import Background
from instruction import Instruction
from obstacle import Obstacle
from sound import Sound
from treasure import Treasure
from start_menu import StartMenu
from game_over import GameOver
from game_stats import GameStat
from scoreboard import ScoreBoard
from ship import Ship

def load_high_score():
    """A function to read high score file."""
    try:
        with open("High_score", "r") as f:
            high_score = json.load(f)
    except FileNotFoundError or json.JSONDecodeError:
        high_score = 0
    return high_score

def save_high_score(self):
    """A function to save high score."""
    with open("High_score", "w") as f:
        json.dump(self.stats.high_score, f)

class SpaceDodge:
    """A class to initialize and maintain game resources."""

    def __init__(self):
        """Initialize the Game Attributes."""
        pygame.init()
        self.settings = Setting()
        self.sound = Sound(self)

        self.world = pygame.Surface((4500, 4500))
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.game_name)

        self.stats = GameStat()
        self.start_menu = StartMenu(self)
        self.instruction = Instruction(self)
        self.gameover = GameOver(self)
        self.clock = pygame.time.Clock()
        self.treasure = Treasure(self, r"images\diamond.png")
        self.scoreboard = ScoreBoard(self)
        self._create_background()
        self.obstacle_group = pygame.sprite.Group()
        self._create_obstacle()
        self.ship = Ship(self)
        self.ship_sprite = pygame.sprite.Group(self.ship)
        self.camera_offset = self.ship.pos - pygame.Vector2(self.settings.screen_width // 2, self.settings.screen_height // 2)

        self.stats.high_score = load_high_score()

        self.game_active = False
        self.game_over = False
        self.instruction_flag = False
        
        self.sound.play_background_music()

    def run_game(self):
        """Run Game Loop."""
        while True:
            self._check_events()
            if self.game_active:
                self._check_treasure_ship_collision()
                self._check_obstacle_ship_collision()
                self._update_sprites()
            self._update_screen()
            self.clock.tick(60)
    
    def _check_events(self):
        """A Method to check keyboard and mouse response"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                
        self.keys = pygame.key.get_pressed()
        self.ship_sprite.update(self.keys)

    def _check_keydown_events(self, event):
        """A method to respond to keypress."""
        if event.key == pygame.K_q:
            save_high_score(self)
            sys.exit()
        if event.key == pygame.K_BACKSPACE:
            if self.game_over:
                self.game_over = False
            if self.instruction_flag:
                self.instruction_flag = False
            self.game_active = False
        if event.key == pygame.K_p:
            self.game_active = True
            self.sound.play_background_music()
            self.sound.stop_game_over_sound()
            self.game_over = False
        if event.key == pygame.K_h:
            if not self.game_active and not self.game_over:
                self.instruction_flag = True


    def _create_background(self):
        """ A method to initialize the background."""
        self.background = Background(self, r"images\background.png")
        self.sun = Background(self, r"images\sun.png", (250, 250), (200, 50))
        self.planet_1 = Background(self, r"images\planet_1.png", (100,100), (2400, 2400))
        self.planet_2 = Background(self, r"images\planet_2.png", (20, 20), (500, 500))
        self.planet_3 = Background(self, r"images\planet_3.png", (140, 140), (3000, 2000))
        self.planet_4 = Background(self, r"images\planet_4.png", (170, 170), (2000, 1357))
        self.planet_5 = Background(self, r"images\planet_5.png", (100, 100), (2598, 4300))
        self.planet_6 = Background(self, r"images\planet_6.png", (200, 200), (800, 800))
        self.planet_7 = Background(self, r'images\planet_7.png', (150, 150), (3500, 3500))
        self.planet_8 = Background(self, r"images\planet_8.png", (35, 35), (1500, 2500))
        self.space_station = Background(self, r"images\bg_ship_image.png", (500, 700), (900, 3000))

    def _create_obstacle(self):
        """A method to create obstacle"""
        obstacle_paths = [
            r"images\rock_1.png",
            r"images\rock.png",
            r"images\star.png",
            r"images\star.png"
            ]

        for _ in range(10):
            for path in obstacle_paths:
                obstacle = Obstacle(self, path)
                self.obstacle_group.add(obstacle)


    def draw_minimap(self):
        """A method to draw minimap."""
        map_size = 100
        minimap = pygame.Surface((map_size, map_size))
        minimap.fill((20, 20, 20))

        scale_x = map_size / self.world.get_width()
        scale_y = map_size / self.world.get_height()

        #draw obstical
        for obstacle in self.obstacle_group:
            mini_x = int(obstacle.pos.x * scale_x)
            mini_y = int(obstacle.pos.y * scale_y)
            pygame.draw.circle(minimap, (200, 0, 0), (mini_x, mini_y), 2)

        # Draw the ship
        mini_ship_x = int(self.ship.pos.x * scale_x)
        mini_ship_y = int(self.ship.pos.y * scale_y)
        pygame.draw.circle(minimap, (0, 255, 0), (mini_ship_x, mini_ship_y), 3)  # green dot for ship

        # draw treasure
        mini_treasure_x = int(self.treasure.pos.x * scale_x)
        mini_treasure_y = int(self.treasure.pos.y * scale_y)
        pygame.draw.circle(minimap, (0, 0, 255), (mini_treasure_x, mini_treasure_y), 3) # blue dot for treasure

        # Draw border
        pygame.draw.rect(minimap, (255, 255, 255), minimap.get_rect(), 1)

        # Blit minimap on main screen (bottom-right corner)
        self.screen.blit(minimap, (self.settings.screen_width - map_size - 10,
            self.settings.screen_height - map_size - 10))
    
    def _check_treasure_ship_collision(self):
        """A method to increase score."""
        if self.ship.rect.colliderect(self.treasure.rect):
            self.treasure.relocate()
            self.stats.score += 1
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()
            if int(self.stats.high_score) % 4 == 0 and self.stats.score != 0:
                self._increase_speed()
        
    def _check_obstacle_ship_collision(self):
        """A method to check collision between ship and obstacles."""
        collision = pygame.sprite.spritecollideany(self.ship, self.obstacle_group)
        if collision:
            sleep(0.6)
            self.stats.reset_game()
            self.game_active = False
            self.game_over = True
            self.instruction_flag = False
            self.ship.reset()
            self.obstacle_group.empty()
            self._create_obstacle()
            self.treasure.relocate()
            self.scoreboard.prep_score()
            self.sound.play_game_over_sound()
            self.sound.stop_background_music()

    def _increase_speed(self):
        """A method to increase ship and treasure speed."""
        self.stats.treasure_speed += 1
        self.stats.ship_speed += 0.8

    def _manage_coordinate(self):
        """Render and blit the ship's coordinates on the screen."""
        font = pygame.font.Font(None, 24)  # Use a slightly larger font
        coordinate_text = f"X: {int(self.ship.pos.x)}  Y: {int(self.ship.pos.y)}"
        text_surface = font.render(coordinate_text, True, (255, 255, 255))  # White color
        self.screen.blit(text_surface, (10, 10))  # Top-left corner

    
    def _background_images(self):
        """A helping method to manage background image."""
        self.background.draw_bg_image()
        self.sun.draw_bg_image()
        self.space_station.draw_bg_image()
        self.planet_1.draw_bg_image()
        self.planet_2.draw_bg_image()
        self.planet_3.draw_bg_image()
        self.planet_4.draw_bg_image()
        self.planet_5.draw_bg_image()
        self.planet_6.draw_bg_image()
        self.planet_7.draw_bg_image()
        self.planet_8.draw_bg_image()

    def _update_sprites(self):
        """A helping method to handel anything related to ship"""
        self.ship.update_ship(self.keys)
        self.treasure.update()
        self.obstacle_group.update()

    def _update_screen(self):
        """A method to update screen."""
        self.world.fill((0, 0, 0))  # Or black or any space color
        self.screen.fill((0, 0, 0))

        # Draw everything to the world surface
        self._background_images()      # Draw background & planets on world
        self.obstacle_group.draw(self.world)
        self.treasure.blit_treasure()
        self.ship_sprite.draw(self.world)   

        # Recalculate camera offset (after ship moves)
        self.camera_offset = self.ship.pos - pygame.Vector2(
            self.settings.screen_width // 2, self.settings.screen_height // 2
        )

        # Draw world surface to screen, offset so ship stays centered
        self.screen.blit(self.world, (-self.camera_offset.x, -self.camera_offset.y))
        self._manage_coordinate()       
        self.scoreboard.draw_score() 
        self.draw_minimap()

        if self.game_over:
            self.gameover.draw_game_over()

        if not self.game_active and not self.game_over:
            self.start_menu.draw_start_menu()
        
        if not self.game_active and self.instruction_flag:
            self.instruction.draw()

        pygame.display.update()

if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = SpaceDodge()
    ai.run_game()