import pygame as pg
from pygame import draw, font, sprite
import time, random, os

pg.init()

pg.display.init()

screen_width=700
screen_height=400
screen=pg.display.set_mode([screen_width, screen_height])

pg.key.set_repeat(500, 30)

fps = 60

currentY = screen_height/2
currentX = screen_width/2

grav = True
velY = 0
Max = 20 
holeSize = 150
speed = 2

pg.display.update()

genHole = lambda: random.randint(10, screen_height-(holeSize-10))

pipes = [screen_width]
pHole = [genHole()]

def dead():
    pg.font.init()
    font = pg.font.Font('freesansbold.ttf', 32)
    text = font.render('Game over', True, (116, 114, 158))
    rect = text.get_rect()
    rect.center = (screen_width//2, screen_height//2)
    screen.fill((0,0,0))
    screen.blit(text, rect)
    while True:
        for event in pg.event.get():
            if event == pg.QUIT:
                pg.quit()
                quit()
        pg.display.update()

started = False

class Player(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, picture="player.png"):
        super().__init__()
        self.image = pg.image.load(picture)
        self.image = pg.transform.smoothscale(self.image, (20,30))

        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
    def move(self, pos_x, pos_y):
        self.rect.center = (pos_x, pos_y)

playerSprite = Player(screen_width//2, screen_height//2)
playerGroup = pg.sprite.Group()
playerGroup.add(playerSprite)

going = True
while going:
    ## GET PLAYER INPUT AND APPLY VELOCITY
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                velY += (Max-velY)*0.5
                if velY > Max:
                    velY = Max
                break
    ## DO MATH :)
    if grav:
        currentY += velY
        if velY > -10 and currentY > 0:
            velY -= 0.5
        if currentY < 0:
            currentY = 0
        # print(currentY)
    screen.fill((0,0,0))

    ## GENERATE AND MOVE PIPE(S)
    if pipes[-1] < screen_width-150:
        pipes += [screen_width]
        pHole += [genHole()]

    if pipes[0] < 20:
        pipes.pop(0)
        pHole.pop(0)
    pHoleOBJ = []
    pipesOBJ = []
    for ind, i in enumerate(pipes):
        pipes[ind] -= speed
        pipesOBJ += [[pg.draw.rect(screen, (0, 255, 0), [i,0,20,pHole[ind]]), pg.draw.rect(screen, (0, 255, 0), [i, pHole[ind]+holeSize, 20, screen_height])]]
        #pHoleOBJ += [pg.draw.rect(screen, (0, 0, 0), [pipes[ind],pHole[ind],20,holeSize])]

    ## MOVE PLAYER
    startX = screen_width - currentX - 10
    startY = screen_height - currentY - 10
    playerSprite.move(startX, startY)
    screen.blit(playerSprite.image, playerSprite.rect)

    ## HIT DETECTION
    for x in pipesOBJ:
        if playerSprite.rect.colliderect(x[0]) or playerSprite.rect.colliderect(x[1]):
            print("Player hit pipe")
            dead()
            going = False
            break

    ## wait till next frame
    time.sleep(1/fps)
    pg.display.update()