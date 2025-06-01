class Settings:
    def __init__(self,s_game):
        """Initialize the game settings"""
        self.s_game = s_game
        # set the screen dimension and color
        self.screen_width = 1000
        self.screen_height = 500
        self.bg_color = (0, 0, 0)

        # wall settings
        self.wall_width = 23
        self.wall_color = (0, 0, 0)

        # set the snake and food colors, sixe, speed
        self.snake_color = (251, 231, 200)
        self.food_color = (255, 255, 204)
        self.snake_size = 20
        self.snake_speed = 2

        # set the font size 
        self.font_size = 33

        # set the game over and score text and color
        self.game_over_text = "Game over!"
        self.game_over_text_color = (255, 0, 0)
        self.game_over_text_size = 100

        self.score = 0
        self.score_text = "Score:"
        self.score_text_color = (255, 255, 255)

        self.high_score = 0
        self.high_score_text = "High Score: "
        self.high_score_color = (211,211,211)