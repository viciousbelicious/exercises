import pygame, sys
from random import *

pygame.init() 
screen = pygame.display.set_mode((350,600))
clock = pygame.time.Clock()

#set game name n icon
pygame.display.set_caption('sand spawner')
#new_icon = pygame.image.load('graphics/icon/icon.png').convert_alpha()
#pygame.display.set_icon(new_icon)

sand_colors = [(249, 65, 68), (243, 114, 44), (248, 150, 30), (249, 132, 74), (249, 199, 79), (144, 190, 109), (67, 170, 139), (77, 144, 142), (87, 117, 144), (39, 125, 161)]
'''
#sand_colors[
Imperial red, 
Orange (Crayola), 
Carrot orange, 
Coral, 
Saffron, 
Pistachio, 
Zomp, 
Dark cyan, 
Payne's gray, 
Cerulean]
'''

class Sand(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface(size) #set sand dimentions
        self.image.fill(choice(sand_colors)) #random colours choice
        self.rect = self.image.get_rect(topleft=pos)
        self.gravity = 0
        self.is_solid = True
        self.border_color = (0, 0, 0)  #colore del bordo


    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 600:
            self.rect.bottom = 600
            
    def collision(self, all_sprites):
        for sprite in all_sprites:
            if sprite != self and pygame.sprite.collide_rect(self, sprite):
                self.rect.y = sprite.rect.y - self.rect.height  
    #check collision of sands blocks

    def update(self):
        self.apply_gravity()
        self.collision(all_sprites)

all_sprites = pygame.sprite.Group()

#blocks spawn delay
spawn_timer = pygame.time.get_ticks()
spawn_delay = 200 #0.2 sec

while True:  #how to run the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    mouse_pressed = pygame.mouse.get_pressed()

    if mouse_pressed[0]:  #if the mouse botton is pressed
        current_time = pygame.time.get_ticks()
        if current_time - spawn_timer >= spawn_delay:
           pos = pygame.mouse.get_pos()
           size_tiles = 20, 20
           sand_block = Sand(pos, size_tiles)
           all_sprites.add(sand_block)
           spawn_timer = current_time

    screen.fill('black')
    all_sprites.update()
    all_sprites.draw(screen)
    
    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)
