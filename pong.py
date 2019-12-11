import pygame, constants, render, random

def handle_keys(key):
    if key == pygame.K_UP:
        return {"movement": "up"}
    elif key == pygame.K_DOWN:
        return {"movement": "down"}
    elif key == pygame.K_ESCAPE:
        return {"escape": True}
    elif key == pygame.K_SPACE or key == pygame.K_RETURN:
        return {"confirm": True}
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
        self.ball = Entity("ball", constants.GAME_WINDOW_WIDTH/2, constants.GAME_WINDOW_HEIGHT/2)
        #ball starts off going either left or right, randomly
        self.reset_ball()
        self.score = [0,0]
        self.winner = None
    
    def reset_ball(self):
        self.ball.x = constants.GAME_WINDOW_WIDTH/2
        self.ball.y = constants.GAME_WINDOW_HEIGHT/2
        self.ball.dx = constants.BALL_SPEED * random.choice((-1,1))
        self.ball.dy = constants.BALL_SPEED * random.choice((-1,1))
        
    def update_score(self):
        renderer.surfaces.left_score = renderer.surfaces.create_score(self.score[0])
        renderer.surfaces.right_score = renderer.surfaces.create_score(self.score[1])
        
    def increment_score(self, scorer):
        self.score[scorer] += 1
        self.update_score()
        
    def check_winner(self):
        if self.score[0] > constants.SCORE_LIMIT:
            self.winner =  "player"
        elif self.score[1] > constants.SCORE_LIMIT:
            self.winner = "ai"
    
    def main_loop(self):
        while self.loop:
            #accept input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.loop = False
                    
                elif event.type == pygame.KEYDOWN and self.game_state == "MENU":
                    action = handle_keys(event.key)
                    escape, confirm = action.get("escape"), action.get("confirm")
                    if escape:
                        self.loop = False
                    if confirm:
                        self.game_state = "GAMEPLAY"
                        self.reset_ball()
                        print("TETAT")      
                        
                elif event.type == pygame.KEYDOWN and self.game_state == "GAMEPLAY":
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
            if self.game_state == "GAMEPLAY":
                #ball movement
                self.ball.x += self.ball.dx
                self.ball.y += self.ball.dy
                
                #ball collision
                #wall collision
                if self.ball.y <= 0:
                    self.ball.dy *= -1
                elif self.ball.y >= constants.GAME_WINDOW_HEIGHT:
                    self.ball.dy *= -1
                
                #paddle collision
                if self.ball.dx < 0:
                    #ball encounters player paddle x coordinate
                    if self.ball.x <= self.player_paddle.x:
                        if (self.ball.y + constants.BALL_HEIGHT) > self.player_paddle.y and self.ball.y < (self.player_paddle.y + constants.PADDLE_HEIGHT):
                            self.ball.dx *= -1
                            self.ball.dy *= -1
                        else:
                            self.reset_ball()
                            self.increment_score(1)
                            self.check_winner()
                else:
                    #ball encounters ai paddle x coordinate
                    if (self.ball.x + constants.BALL_WIDTH) >= (self.ai_paddle.x + constants.PADDLE_WIDTH):
                        if (self.ball.y + constants.BALL_HEIGHT) > self.ai_paddle.y and self.ball.y < (self.ai_paddle.y + constants.PADDLE_HEIGHT):
                            self.ball.dx *= -1
                            self.ball.dy *= -1
                        else:
                            self.reset_ball()
                            self.increment_score(0)
                            self.check_winner()
                
                if not self.winner == None:
                    if self.winner == "player":
                        self.game_state = "MENU"
                    elif self.winner == "ai":
                        self.game_state = "MENU"  
                    self.winner = None
                    self.score = [0,0]
                    self.update_score()
            
            #draw game
            self.gameDisplay.fill((0,0,0))
            if self.game_state == "GAMEPLAY":
                #draw the midline
                renderer.render_object(renderer.surfaces.midline, (constants.GAME_WINDOW_WIDTH/2 - constants.MIDLINE_WIDTH/2, 0))
                #draw the score
                renderer.render_object(renderer.surfaces.left_score, (constants.SCORE_X_L, constants.SCORE_Y))
                renderer.render_object(renderer.surfaces.right_score, (constants.SCORE_X_R, constants.SCORE_Y))
                #draw the player
                renderer.render_object(renderer.surfaces.player_paddle, (self.player_paddle.x, self.player_paddle.y))
                #draw the ai
                renderer.render_object(renderer.surfaces.ai_paddle, (self.ai_paddle.x, self.ai_paddle.y))
                #draw the ball
                renderer.render_object(renderer.surfaces.ball, (self.ball.x, self.ball.y))
            elif self.game_state == "MENU":
                renderer.render_object(renderer.surfaces.main_menu, (0,0))
                
            pygame.display.update()
            self.clock.tick(self.tick)

if __name__ == "__main__":
    game = Game()
    renderer = render.Renderer(game.gameDisplay)
    game.main_loop()
    pygame.quit()
    quit()
    