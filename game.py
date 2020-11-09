import pygame as pg
from pygame import draw, font, sprite
import time, random, os

pg.init()

pg.display.init()

screen_width=700
screen_height=400

screen=pg.display.set_mode([screen_width, screen_height])

pg.key.set_repeat(500, 30)

fps = 75

currentY = screen_height/2
currentX = screen_width/2

grav = True
velY = 0
Max = 20 
holeSize = 150
speed = 2
thiccnessMultiplier = 2
pipeWideness = 20
distanceBetweenPipes = 200

pg.display.update()

genHole = lambda: random.randint(10, screen_height-(holeSize+10))

# class Scoreboard:
#     def __init__(self):
#         self.score = 0
#         pg.font.init()
    
#     def __add__(self, amount: int):
#         '''
#         adds amount to current score and returns the result
#         WARNING: DO NOT USE += IT WILL NOT WORk
#         '''
#         self.score += amount
#         return self.score + amount

#     def update(self):
#         font = pg.font.Font('freesansbold.ttf', 32)
#         text = font.render(f'{self.score}', True, (116, 114, 158))
#         rect = text.get_rect()
#         rect.center = (screen_width-10, screen_height-26)
#         screen.blit(text, rect)

# def dead():
#     pg.font.init()
#     font = pg.font.Font('freesansbold.ttf', 32)
#     text = font.render('Game over', True, (116, 114, 158))
#     rect = text.get_rect()
#     rect.center = (screen_width//2, screen_height//2)
#     screen.fill((0,0,0))
#     screen.blit(text, rect)
#     while True:
#         for event in pg.event.get():
#             if event == pg.QUIT:
#                 pg.quit()
#                 quit()
#         pg.display.update()

# class Player(pg.sprite.Sprite):
#     def __init__(self, pos_x, pos_y, picture="player.png"):
#         super().__init__()
#         self.image = pg.image.load(picture)
#         self.image = pg.transform.smoothscale(self.image, (20*thiccnessMultiplier,30))

#         self.rect = self.image.get_rect()
#         self.rect.center = (pos_x, pos_y)
#     def move(self, pos_x, pos_y):
#         self.rect.center = (pos_x, pos_y)

# playerSprite = Player(screen_width//2, screen_height//2)
# playerGroup = pg.sprite.Group()
# playerGroup.add(playerSprite)

class Pipe:
    def __init__(self, rect):
        self.rect = pg.draw.rect(screen, (0,255,0), rect)
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.surface.fill((0,255,0))
    def update(self, x):
        self.rect.x = self.rect.x + x
        pg.display.update(self.rect)

class Pipes:
    def __init__(self, x=screen_width):
        self.pHole = genHole()
        self.pipes = []
        self.pipes += [Pipe([x, 0, pipeWideness, self.pHole])]

        self.pipes += [Pipe([x, self.pHole+holeSize, pipeWideness, screen_height])]

        self.pipes += [Pipe([x-(int(pipeWideness*0.5)), self.pHole-1, (pipeWideness)*2, 20 ])]

        self.pipes += [Pipe([x-(int(pipeWideness*0.5)), self.pHole+holeSize, (pipeWideness)*2, 20])]

    def move(self, x=1):
        '''
        pass how many pixel you want to move the pipe along the x axis
        '''
        for _,i in enumerate(self.pipes):
            i.update(x)
            if _ == 3:
                print(i.rect.center)
                pass


pipe = Pipes()
while True:
    pg.event.get()
    pipe.move(1)
    time.sleep(1/fps)
    pg.display.update()