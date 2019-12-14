import pygame, constants, render, random, math

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
        
    def reset_ball(self):
        self.speed = constants.BALL_SPEED
        self.x = constants.GAME_WINDOW_WIDTH/2
        self.y = constants.GAME_WINDOW_HEIGHT/2
        self.dx = int(math.cos(math.radians(45)) * (self.speed * random.choice((-1,1))))
        self.dy = int(math.sin(math.radians(45)) * (self.speed * random.choice((-1,1))))
        
    def ball_collision(self, paddle):
        #if the ball hits the 'middle'  it bounces straight. closer to the edge = bigger angle. if it hits the 'edge', it bounces at max angle of 70.
        ball_center = self.y + constants.BALL_HEIGHT/2
        paddle_center = paddle.y + constants.PADDLE_HEIGHT/2
        distance_from_center = int(ball_center - paddle_center)
        angle_to_bounce = int((distance_from_center/(constants.PADDLE_HEIGHT/2 + constants.BALL_HEIGHT/2)) * 70)
        angle_in_rads = math.radians(angle_to_bounce)
        #increase ball speed a tiny bit each bounce
        self.speed += constants.BALL_BOUNCE_ACCELERATION
        #check which way to send the ball, based on its speed before collision
        if self.dx > 0:
            self.dx = int(-1 * math.cos(angle_in_rads) * self.speed) 
        else:
            self.dx = int(math.cos(angle_in_rads) * self.speed)
        self.dy = int(math.sin(angle_in_rads) * self.speed)        

    def paddle_ai(self, ball):
        #ai will constantly try to center the paddle on the ball. add or subtract constants.BALL_HEIGHT to prevent the ai from "flickering"
        paddle_center = (self.y + constants.PADDLE_HEIGHT/2)
        if ball.y > paddle_center + constants.BALL_HEIGHT/2:
            self.move(0, constants.PADDLE_SPEED)
            if self.y + constants.PADDLE_HEIGHT > constants.GAME_WINDOW_WIDTH:
                self.y = constants.GAME_WINDOW_WIDTH - constants.PADDLE_HEIGHT            

        elif ball.y < paddle_center - constants.BALL_HEIGHT/2:
            self.move(0, -constants.PADDLE_SPEED)
            if self.y < 0:
                self.y = 0  
class Game:
    def __init__(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((constants.GAME_WINDOW_WIDTH, constants.GAME_WINDOW_HEIGHT))
        pygame.display.set_caption("PONG")
        self.loop = True
        self.tick = 60
        self.clock = pygame.time.Clock()
        self.game_state = constants.GAMESTATE_MENU
        pygame.key.set_repeat(int(1000/self.tick))
        self.player_paddle = Entity("player", 50, constants.GAME_WINDOW_HEIGHT/2)
        self.ai_paddle = Entity("ai", constants.GAME_WINDOW_WIDTH - 50, constants.GAME_WINDOW_HEIGHT/2)
        self.ball = Entity("ball", constants.GAME_WINDOW_WIDTH/2, constants.GAME_WINDOW_HEIGHT/2)
        #ball starts off going either left or right, randomly
        self.ball.reset_ball()
        self.score = [0,0]
        self.winner = None
    
    def reset_paddles(self):
        self.player_paddle.y = constants.GAME_WINDOW_HEIGHT/2
        self.ai_paddle.y = constants.GAME_WINDOW_HEIGHT/2
        
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
            
    def win_lose(self):
        #pops up a screen for 3 seconds
        counter = 0
        while counter < 180:
            counter += 1
            print("LOSER!")
            self.clock.tick(self.tick)          
    
    def main_loop(self):
        while self.loop:
            #accept input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.loop = False
                    
                elif event.type == pygame.KEYDOWN and self.game_state == constants.GAMESTATE_MENU:
                    action = handle_keys(event.key)
                    escape, confirm = action.get("escape"), action.get("confirm")
                    if escape:
                        self.loop = False
                    if confirm:
                        self.game_state = constants.GAMESTATE_GAMEPLAY
                        self.ball.reset_ball()

                elif event.type == pygame.KEYDOWN and self.game_state == constants.GAMESTATE_GAMEPLAY:
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
            
            #game logic
            if self.game_state == constants.GAMESTATE_GAMEPLAY:
                #ai paddle logic
                self.ai_paddle.paddle_ai(self.ball)
                
                #ball movement
                self.ball.move(self.ball.dx, self.ball.dy)
                
                #wall collision
                if self.ball.y <= 0 or (self.ball.y + constants.BALL_HEIGHT) >= constants.GAME_WINDOW_HEIGHT:
                    self.ball.dy *= -1
                
                #paddle collision
                if self.ball.dx < 0:
                    #ball encounters player paddle x coordinate
                    if self.ball.x <= self.player_paddle.x:
                        if (self.ball.y + constants.BALL_HEIGHT) >= self.player_paddle.y and self.ball.y <= (self.player_paddle.y + constants.PADDLE_HEIGHT):
                            self.ball.ball_collision(self.player_paddle)
                        else:
                            self.ball.reset_ball()
                            self.reset_paddles()
                            self.increment_score(1)
                            self.check_winner()
                else:
                    #ball encounters ai paddle x coordinate
                    if (self.ball.x + constants.BALL_WIDTH) >= (self.ai_paddle.x + constants.PADDLE_WIDTH):
                        if (self.ball.y + constants.BALL_HEIGHT) >= self.ai_paddle.y and self.ball.y <= (self.ai_paddle.y + constants.PADDLE_HEIGHT):
                            self.ball.ball_collision(self.ai_paddle)
                        else:
                            self.ball.reset_ball()
                            self.reset_paddles()
                            self.increment_score(0)
                            self.check_winner()
                
                #if there's a winner, go back to main menu and reset score for the next game.
                if not self.winner == None:
                    if self.winner == "player":
                        self.game_state = constants.GAMESTATE_MENU
                    elif self.winner == "ai":
                        self.game_state = constants.GAMESTATE_MENU  
                    self.winner = None
                    self.score = [0,0]
                    self.update_score()
            
            #draw game
            self.gameDisplay.fill((0,0,0))
            if self.game_state == constants.GAMESTATE_GAMEPLAY:
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
            elif self.game_state == constants.GAMESTATE_MENU:
                renderer.render_object(renderer.surfaces.main_menu, (0,0))
                
            elif self.game_state == constants.GAMESTATE_OPTIONS:
                pass
            elif self.game_state == constants.GAMESTATE_EXIT_PROMPT:
                pass
                
            pygame.display.update()
            self.clock.tick(self.tick)

if __name__ == "__main__":
    game = Game()
    renderer = render.Renderer(game.gameDisplay)
    game.main_loop()
    pygame.quit()
    quit()
    