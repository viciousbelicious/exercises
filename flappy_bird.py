import pygame
import random
import os

# game init
pygame.init()

# load img
back = pygame.image.load(os.path.join("back.png"))
game_over = pygame.image.load(os.path.join("gameover.png"))
ground = pygame.image.load(os.path.join("base.png"))
bird = pygame.image.load(os.path.join("bird.png"))
tube_up = pygame.image.load(os.path.join("tubo.png"))
tube_down = pygame.transform.flip(tube_up, False, True)

# game window
game_window = pygame.display.set_mode((288, 512))
FPS = 50
velo = 3
font = pygame.font.SysFont("Tahoma", 50, bold=True)


class tubi_classe:
    def __init__(self):
        self.x = 300
        self.y = random.randint(-75, 150)
    def mov_tubi(self):
        self.x -= velo
        game_window.blit(tube_up, (self.x, self.y + 210))
        game_window.blit(tube_down, (self.x, self.y - 210))
    def collision(self, bird, birdx, birdy):
        tolleranza = 5
        dx_bird = birdx + bird.get_width() - tolleranza
        sx_bird = birdx + tolleranza
        dx_tube = self.x + tube_down.get_width()
        sx_tube = self.x
        up_bird = birdy + tolleranza
        down_bird = birdy + bird.get_height() - tolleranza
        up_tube = self.y + 110
        down_tube = self.y + 210
        if dx_bird > sx_tube and sx_bird < dx_tube:
            if up_bird < up_tube or down_bird > down_tube:
                gameover()
    def between (self, bird, birdx):
        tolleranza = 5
        dx_bird = birdx + bird.get_width() - tolleranza
        sx_bird = birdx + tolleranza
        dx_tube = self.x + tube_down.get_width()
        sx_tube = self.x
        if dx_bird > sx_tube and sx_bird < dx_tube:
            return True

def draw_item(): # dove sono gli item nella finestra
    game_window.blit(back, (0,0))
    for t in tubes:
        t.mov_tubi()
    game_window.blit(bird, (birdx,birdy))
    game_window.blit(ground, (groundx,400))
    points_render = font.render(str(points), 1, (255,255,255))
    game_window.blit(points_render, (140, 5))

def refresh():
    pygame.display.update()
    pygame.time.Clock().tick(FPS)    

def start(): # condizioni di partenza, coordinate del pg
    global birdx, birdy, bird_vel
    global groundx
    global tubes
    global points
    global between
    birdx, birdy = 60, 150
    bird_vel = 0
    groundx = 0
    points = 0
    tubes = []
    tubes.append(tubi_classe())
    between = False

def gameover():
    game_window.blit(game_over, (50,180))
    refresh()
    restart = False
    while not restart:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start()
                restart = True
            if event.type == pygame.QUIT:
                pygame.quit()

start()

while True:
    groundx -= velo
    if groundx < -45: groundx = 0
    bird_vel += 1 # gravity
    birdy += bird_vel
    for event in pygame.event.get():
        if ( event.type == pygame.KEYDOWN
            and event.key == pygame.K_UP ):
           bird_vel = -10
        if event.type == pygame.QUIT:
             pygame.quit()
        if tubes[-1].x < 150: tubes.append(tubi_classe()) # tubi
        for t in tubes: # gameover on tubes
            t.collision(bird, birdx, birdy)
    if not between:
        for t in tubes:
            for t in tubes:
                if t.between(bird,birdx):
                    between = True
    if between:
        between = False
        for t in tubes:
            if t.between(bird,birdx):
                between = True
                break
        if not between:
            points += 1
    if birdy > 380: #gameover on ground
        gameover()

    #refresh
    draw_item()
    refresh()