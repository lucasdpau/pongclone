import pygame,constants

class GameSurfaces:
    def __init__(self):
        self.font = pygame.font.SysFont(constants.GAME_FONT, constants.GAME_FONT_SIZE)
        self.score_font = pygame.font.SysFont(constants.GAME_FONT, constants.SCORE_FONT_SIZE)
        self.ball = self.create_ball()
        self.player_paddle = self.create_paddle()
        self.ai_paddle = self.create_paddle()
        self.left_score = self.create_score(0)
        self.right_score = self.create_score(0)
        self.midline = self.create_midline()
        
    def create_ball(self):
        ball = pygame.Surface((constants.BALL_WIDTH, constants.BALL_HEIGHT))
        ball.fill((255, 255, 255))
        return ball
    
    def create_paddle(self):
        paddle = pygame.Surface((constants.PADDLE_WIDTH, constants.PADDLE_HEIGHT))
        paddle.fill((255, 255, 255))
        return paddle
    
    def create_score(self, score):
        score_string = str(score)
        score_surface = self.score_font.render(score_string, False, (100,100,100))
        return score_surface
        
    
    def create_midline(self):
        midline = pygame.Surface((constants.MIDLINE_WIDTH, constants.GAME_WINDOW_HEIGHT))
        midline.fill((200, 200, 200))
        return midline

class Renderer:
    def __init__(self, main_surface):
        self.surfaces = GameSurfaces()
        self.main_surface = main_surface
    
    def render_object(self, surface_to_blit, object_location):
        self.main_surface.blit(surface_to_blit, object_location)
        