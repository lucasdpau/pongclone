import pygame, constants, render

class Entity:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0

class Game:
    def __init__(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((constants.GAME_WINDOW_WIDTH, constants.GAME_WINDOW_HEIGHT))
        pygame.display.set_caption("PONG")
        self.loop = True
        self.tick = 30
        self.clock = pygame.time.Clock()
        self.game_state = "MENU"
        
    def main_loop(self):
        while self.loop:
            #accept input
            #update game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.loop = False
                elif event.type == pygame.KEYDOWN:
                    pass
            
            
            #draw game
            self.gameDisplay.fill((0,0,0))
            pygame.display.update()
            self.clock.tick(self.tick)

if __name__ == "__main__":
    game = Game()
    renderer = render.Renderer(game.gameDisplay)
    game.main_loop()
    pygame.quit()
    quit()
    