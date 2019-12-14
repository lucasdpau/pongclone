import pygame, constants, render, random, math

def handle_keys(key):
    if key == pygame.K_UP:
        return {"movement_R": "up"}
    elif key == pygame.K_DOWN:
        return {"movement_R": "down"}
    elif key == pygame.K_w:
        return {"movement_L": "up"}
    elif key == pygame.K_s:
        return {"movement_L": "down"}
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
        self.prev_x = 0
        self.y = y
        self.prev_y = 0
        self.dx = 0
        self.dy = 0
    
    def move(self, dx, dy):
        self.prev_x = self.x
        self.x += dx
        self.prev_y = self.y
        self.y += dy
        
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
        self.left_paddle = Entity("player", 50, constants.GAME_WINDOW_HEIGHT/2)
        self.right_paddle = Entity("ai", constants.GAME_WINDOW_WIDTH - 50, constants.GAME_WINDOW_HEIGHT/2)
        self.ball = Entity("ball", constants.GAME_WINDOW_WIDTH/2, constants.GAME_WINDOW_HEIGHT/2)
        #ball starts off going either left or right, randomly
        self.ball.reset_ball()
        self.score = [0,0]
        self.winner = None
        self.players = 2
    
    def reset_paddles(self):
        self.left_paddle.y = constants.GAME_WINDOW_HEIGHT/2
        self.right_paddle.y = constants.GAME_WINDOW_HEIGHT/2
        
    def update_score(self):
        renderer.surfaces.left_score = renderer.surfaces.create_score(self.score[0])
        renderer.surfaces.right_score = renderer.surfaces.create_score(self.score[1])
        
    def increment_score(self, scorer):
        self.score[scorer] += 1
        self.update_score()
        
    def check_winner(self):
        if self.score[0] > constants.SCORE_LIMIT:
            self.winner =  "left"
        elif self.score[1] > constants.SCORE_LIMIT:
            self.winner = "right"
            
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
                    right_paddle_movement = action.get("movement_R")
                    left_paddle_movement = action.get("movement_L")
                    escape = action.get("escape")
                    #paddle movement, with constraints
                    if left_paddle_movement == "up":
                        self.left_paddle.move(0, -constants.PADDLE_SPEED)
                        if self.left_paddle.y < 0:
                            self.left_paddle.y = 0
                    if left_paddle_movement == "down":
                        self.left_paddle.move(0, constants.PADDLE_SPEED)
                        if self.left_paddle.y + constants.PADDLE_HEIGHT > constants.GAME_WINDOW_HEIGHT:
                            self.left_paddle.y = constants.GAME_WINDOW_HEIGHT - constants.PADDLE_HEIGHT
                    
                    if self.players == 2:
                        if right_paddle_movement == "up":
                            self.right_paddle.move(0, -constants.PADDLE_SPEED)
                            if self.right_paddle.y < 0:
                                self.right_paddle.y = 0
                        if right_paddle_movement == "down":
                            self.right_paddle.move(0, constants.PADDLE_SPEED)
                            if self.right_paddle.y + constants.PADDLE_HEIGHT > constants.GAME_WINDOW_HEIGHT:
                                self.right_paddle.y = constants.GAME_WINDOW_HEIGHT - constants.PADDLE_HEIGHT
            
            #game logic
            if self.game_state == constants.GAMESTATE_GAMEPLAY:
                
                if self.players == 1:
                    #ai paddle logic
                    self.right_paddle.paddle_ai(self.ball)
                
                #ball movement
                self.ball.move(self.ball.dx, self.ball.dy)
                
                #wall collision
                if self.ball.y <= 0 or (self.ball.y + constants.BALL_HEIGHT) >= constants.GAME_WINDOW_HEIGHT:
                    self.ball.dy *= -1
                
                #paddle collision
                if self.ball.dx < 0:
                    #ball encounters left paddle x coordinate
                    if self.ball.x <= self.left_paddle.x + constants.PADDLE_WIDTH:
                        #if the ball is too fast it can go past the paddle in between frames. so we keep track of the balls previous x coordinate and see if the paddle is between the current and previous ball x
                        if (self.ball.y + constants.BALL_HEIGHT) >= self.left_paddle.y and self.ball.y <= (self.left_paddle.y + constants.PADDLE_HEIGHT) and self.ball.prev_x >= (self.left_paddle.x + constants.PADDLE_WIDTH) > self.ball.x:
                            self.ball.ball_collision(self.left_paddle)
                        elif self.ball.x <= 0:
                            self.ball.reset_ball()
                            self.reset_paddles()
                            self.increment_score(1)
                            self.check_winner()
                else:
                    #ball encounters right paddle x coordinate
                    if (self.ball.x + constants.BALL_WIDTH) >= self.right_paddle.x:
                        if (self.ball.y + constants.BALL_HEIGHT) >= self.right_paddle.y and self.ball.y <= (self.right_paddle.y + constants.PADDLE_HEIGHT) and self.ball.prev_x <= self.right_paddle.x <= self.ball.x:
                            self.ball.ball_collision(self.right_paddle)
                        elif self.ball.x >= constants.GAME_WINDOW_WIDTH:
                            self.ball.reset_ball()
                            self.reset_paddles()
                            self.increment_score(0)
                            self.check_winner()
                
                #if there's a winner, go back to main menu and reset score for the next game.
                if not self.winner == None:
                    if self.winner == "left":
                        self.game_state = constants.GAMESTATE_MENU
                    elif self.winner == "right":
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
                renderer.render_object(renderer.surfaces.left_paddle, (self.left_paddle.x, self.left_paddle.y))
                #draw the ai
                renderer.render_object(renderer.surfaces.right_paddle, (self.right_paddle.x, self.right_paddle.y))
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
    