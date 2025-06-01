import sys
import json
from time import sleep

import pygame

from sound_effect import SoundEffect
from setting import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from background import Background 

def load_high_score():
    """Load high score from a file."""
    try:
        with open("high_score.json", "r") as f:
            high_score = json.load(f)
    except FileNotFoundError or json.JSONDecodeError:
        high_score = 0
    return high_score

def save_high_score(self):
    """save high score to a file."""
    with open("high_score.json", "w") as f:
        json.dump(self.stats.high_score, f)

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self): # construction method 
        """Initialize the game, and create game resources."""
        pygame.init()  # Initialize background settings like sound and graphics
        self.settings = Settings()
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # create an instance of effect of the game.
        self.bg = Background(self, "images/planet.jpg")
        self.alien_face = Background(self, "images/alien_face.jpg", (210, 210))
        self.explosion_image = Background(self, "images/explosion.png", (100, 100),)

        # create an instance to store game statistics.
        self.stats = GameStats(self) 
        self.sb = Scoreboard(self)
        # Create a ship instance
        self.ship = Ship(self)
        self.sound_effect = SoundEffect(self)

        # Create groups to store bullets and aliens
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # flag to work with mode button
        self.selection_mode = False
        # flag for game over mode
        self.game_over = False
        # start alieninvasion in inactive state
        self.game_active = False
        
        # create the play button
        self.welcome_text = Button(self, "Alien Invasion", -60, 70, (60, 220, 110), (0, 0, 0))
        self.play_button = Button(self, "Play", None, 48)
        self.Mode_button = Button(self, "Mode", 53, 48)
        # buttons in Mode buton.
        self.relax_mode = Button(self, "Relax", -53, 48)
        self.normal_mode = Button(self, "Chill", None, 48)
        self.insane_mode = Button(self, "Insane", 53, 48)
        # game over and play 
        self.game_over_button = Button(self, "Game over", None, 200, (255, 255, 255) , (0, 0, 0))
    
        self._create_fleet() if self.game_active else None
        self.stats.high_score = load_high_score()
        self.sb.prep_high_score()
        self.sound_effect.play_background_music()


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()     # Respond to keyboard/mouse input

            if self.game_active:
                self.ship.update()       # Update ship's position
                self._update_bullets()   # Update bullets and remove old ones
                self._update_aliens()    # Move aliens
            
            self._update_screen()    # Draw everything on the screen
            self.clock.tick(60)      # limit the frame rate

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score(self)
                sys.exit()  # Exit game when window is closed
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)  # Handle key pressed
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)    # Handle key released
            elif event.type == pygame.MOUSEBUTTONDOWN: # clicks anywhere on the screen
                mouse_pos = pygame.mouse.get_pos() # return tuple of x, y position
                if self.selection_mode:
                    self._check_mode_button(mouse_pos)
                else:
                    self._check_button(mouse_pos) # check if button is clicked

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True  # Start moving right
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True   # Start moving left
        elif event.key == pygame.K_q:
            save_high_score(self)
            sys.exit()                     # Quit the game
        elif event.key == pygame.K_p:
            if not self.game_active and not self.game_over:
                self._start_game()
        elif event.key == pygame.K_SPACE:
            self.sound_effect.play_bullet_sound()
            self._fire_bullet() if self.game_active else None       
        elif event.key == pygame.K_BACKSPACE:
            if self.selection_mode:
                self.selection_mode = False
                pygame.mouse.set_visible(True)
            if self.game_over:
                self.aliens.empty()
                self.bullets.empty()
                self.game_over = False 
                self.sound_effect.stop_game_over_sound()
                self.sound_effect.play_background_music()
            if self.game_active:
                self.game_active = False
                pygame.mouse.set_visible(True)
                self.stats.reset_game()
        

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False  # Stop moving right
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False   # Stop moving left

    def _check_button(self, mouse_pos):
        """Start a new game when the player clicks play"""
        play_button_clicked =  self.play_button.rect.collidepoint(mouse_pos)
        mode_button_clicked = self.Mode_button.rect.collidepoint(mouse_pos)

        if play_button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self._start_game()
        if mode_button_clicked and not self.game_active:
            self.game_active = False 
            self.selection_mode = True

    def _start_game(self):
        """start game after player enter p or click on play btton"""
        # reset the game statistics
        self.stats.reset_game()
        self.game_active = True

        # hide the mouse cursor
        pygame.mouse.set_visible(False) 

        # create a new fleet 
        self._create_fleet()

    def game_mode(self):
        """display game mode selection"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.sb.show_score()

        self.relax_mode.draw_button()
        self.normal_mode.draw_button()
        self.insane_mode.draw_button()

        pygame.display.update()
        self.clock.tick(60)
    
    def game_over_mode(self):
        """display game over message and play button"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.sb.show_score()

        self.game_over_button.draw_button()
        self.sound_effect.play_game_over_sound()

        pygame.display.update()
        self.clock.tick(60)        

    def _check_mode_button(self, mouse_pos):
        """Display mode selection and handle mode click."""
        if self.relax_mode.rect.collidepoint(mouse_pos):
            self.settings.mode_settings("relax")
            self._start_game()
            self.selection_mode = False
        elif self.normal_mode.rect.collidepoint(mouse_pos):
            self.settings.mode_settings("Chill")
            self._start_game()
            self.selection_mode = False
        elif self.insane_mode.rect.collidepoint(mouse_pos):
            self.settings.mode_settings("Insane")
            self._start_game()
            self.selection_mode = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()

        # Remove bullets that have gone off-screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collision()      

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # create an alien and keepin adding untill no space is left.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size # get the size of the alien.

        current_x, current_y = alien_width, alien_height + 30 # set the starting position of the alien.
        while current_y < (self.settings.screen_height - 3 * alien_height): 
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width 

            current_x = alien_width
            current_y += 2 * (alien_height)
       
    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""
        new_alien = Alien(self)
        new_alien.x = x_position        # set the x position of the alien
        new_alien.rect.x = x_position   # set the rect x position of the alien
        new_alien.rect.y = y_position   # set the rect y position of the alien
        self.aliens.add(new_alien)
    
    def _check_bullet_alien_collision(self):
        """check collision between alien and bullet"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            self.sound_effect.play_explosion_sound()
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.explosion_image.update(aliens[0].rect)

            self.sb.prep_score()
            self.sb.check_high_score()

    def _check_fleet(self):
        """check if there is alien"""
        if not self.aliens: # return true if group is empty.
            # Destroy existing blutes and create new fleet.
            self.bullets.empty() # empty method remove all sprite in group.
            self._create_fleet()
            self.settings.increase_speed()

            # increase level 
            self.stats.level += 1
            self.sb.prep_level()

    def _check_fleet_edge(self):
        """respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1 

    def _update_aliens(self):
        """update the position of all the aliens in the fleet"""
        self._check_fleet_edge()
        self.aliens.update()

        # look for alien ship collision.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # pygame.sprite.spritecollideany(sprite, group): return sprite,If no collisions occur, spritecollideany() returns None 
            self._ship_hit()

        # look out for alien that reach bottom
        self._check_aliens_hit_bottoms()
        self._check_fleet()

    def _check_aliens_hit_bottoms(self):
        """ check if alien reached bottom"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # treat this as ship been hit.
                self._ship_hit()
                break

    def _ship_hit(self):
        """respond to the ship being hit by alien"""
        if self.stats.ships_left > 0:
            # Decrement ships_left
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # create a new fleet and centerdd the ship.
            self._create_fleet()
            self.ship.center_ship()

            # pause
            sleep(0.5)
        else:
            self.game_active = False
            self.game_over = True
            self.sound_effect.stop_background_music()
            pygame.mouse.set_visible(True)


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)   # Redraw the background
        self.bg.blitme()
        
        if self.selection_mode:
            self.game_mode()
        elif self.game_over:
            self.game_over_mode()
        else:
            # Draw the play button if the game is inactive
            if not self.game_active:
                self.screen.fill(self.settings.bg_color) 
                self.alien_face.blitme()
                self.alien_face.update((543, 89))
                self.welcome_text.draw_button()
                self.play_button.draw_button()
                self.Mode_button.draw_button()
                self.sb.prep_score()
        
            self.ship.blitme()  # Draw the ship
            # Draw score information
            self.sb.show_score()

            # Draw each bullet
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()

            # Draw the aliens
            self.aliens.draw(self.screen)
            self.explosion_image.blitme()
            self.explosion_image.update((-100, -80))
        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()