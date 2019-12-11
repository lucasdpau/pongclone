import pygame, constants, render, random

def handle_keys(key):
    if key == pygame.K_UP:
        return {"movement": "up"}
    elif key == pygame.K_DOWN:
        return {"movement": "down"}
    else:
        return {}

class Entity:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
    
    def move(self, x, y):
        self.x += x
        self.y += y

class Game:
    def __init__(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((constants.GAME_WINDOW_WIDTH, constants.GAME_WINDOW_HEIGHT))
        pygame.display.set_caption("PONG")
        self.loop = True
        self.tick = 60
        self.clock = pygame.time.Clock()
        self.game_state = "MENU"
        pygame.key.set_repeat(int(1000/self.tick))
        self.player_paddle = Entity("player", 50, constants.GAME_WINDOW_HEIGHT/2)
        self.ai_paddle = Entity("ai", constants.GAME_WINDOW_WIDTH - 50, constants.GAME_WINDOW_HEIGHT/2)
        self.ball = Entity("ball", constants.GAME_WINDOW_WIDTH/2, constants.GAME_WINDOW_WIDTH/2)
        #ball starts off going either left or right, randomly
        self.ball.dx = constants.BALL_SPEED * random.choice((-1,1))
        self.ball.dy = constants.BALL_SPEED * random.choice((-1,1))
    
    def reset_ball(self):
        self.ball.dx = constants.BALL_SPEED * random.choice((-1,1))
        self.ball.dy = constants.BALL_SPEED * random.choice((-1,1))
        pass
    
    def main_loop(self):
        while self.loop:
            #accept input
            #update game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.loop = False
                elif event.type == pygame.KEYDOWN:
                    action = handle_keys(event.key)
                    movement = action.get("movement")
                    #paddle movement, with constraints
                    if movement == "up":
                        if self.player_paddle.y > 0:
                            self.player_paddle.move(0, -constants.PADDLE_SPEED)
                        else:
                            self.player_paddle.y = 0
                    if movement == "down":
                        if self.player_paddle.y + constants.PADDLE_HEIGHT < constants.GAME_WINDOW_HEIGHT:
                            self.player_paddle.move(0, constants.PADDLE_SPEED)
                        else:
                            self.player_paddle.y = constants.GAME_WINDOW_HEIGHT - constants.PADDLE_HEIGHT
            
            
            #ball logic
            #ball movement
            self.ball.x += self.ball.dx
            self.ball.y += self.ball.dy
            
            #ball collision
        
            
            #draw game
            self.gameDisplay.fill((0,0,0))
            #draw the player
            renderer.render_object(renderer.surfaces.player_paddle, (self.player_paddle.x, self.player_paddle.y))
            #draw the ai
            renderer.render_object(renderer.surfaces.ai_paddle, (self.ai_paddle.x, self.ai_paddle.y))
            #draw the ball
            renderer.render_object(renderer.surfaces.ball, (self.ball.x, self.ball.y))
            pygame.display.update()
            self.clock.tick(self.tick)

if __name__ == "__main__":
    game = Game()
    renderer = render.Renderer(game.gameDisplay)
    game.main_loop()
    pygame.quit()
    quit()
    