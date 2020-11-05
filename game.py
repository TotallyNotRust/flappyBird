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

pipes = [screen_width]
pHole = [genHole()]

class Scoreboard:
    def __init__(self):
        self.score = 0
        pg.font.init()
    
    def __add__(self, amount: int):
        '''
        adds amount to current score and returns the result
        WARNING: DO NOT USE += IT WILL NOT WORk
        '''
        self.score += amount
        return self.score + amount

    def update(self):
        font = pg.font.Font('freesansbold.ttf', 32)
        text = font.render(f'{self.score}', True, (116, 114, 158))
        rect = text.get_rect()
        rect.center = (screen_width-10, screen_height-26)
        screen.blit(text, rect)

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

class Player(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, picture="player.png"):
        super().__init__()
        self.image = pg.image.load(picture)
        self.image = pg.transform.smoothscale(self.image, (20*thiccnessMultiplier,30))

        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
    def move(self, pos_x, pos_y):
        self.rect.center = (pos_x, pos_y)

playerSprite = Player(screen_width//2, screen_height//2)
playerGroup = pg.sprite.Group()
playerGroup.add(playerSprite)

sc = Scoreboard()

def makePipes(i, ind):
    yield pg.draw.rect(screen, (0, 255, 0), [i,0,pipeWideness,pHole[ind]])
    yield pg.draw.rect(screen, (0, 255, 0), [i, pHole[ind]+holeSize, pipeWideness, screen_height])
    #[x,y,X,Y]
    yield pg.draw.rect(screen, (0, 255, 0), [i-(pipeWideness*0.5),
                                            pHole[ind]-1,
                                            (pipeWideness)*2,
                                            20
                                            ])
    yield pg.draw.rect(screen, (0, 255, 0), [i-(pipeWideness*0.5), 
                                            pHole[ind]+holeSize, 
                                            (pipeWideness)*2, 
                                            20
                                            ])



going = True
while going:
    sc.update()
    ## GET PLAYER INPUT AND APPLY VELOCITY
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                velY += (Max-velY)*0.5
                if velY > Max:
                    velY = Max
                break
            if event.key == pg.KMOD_SHIFT:
                if velY > 0:
                    velY -= (Max-velY)*0.5
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
    if pipes[-1] < screen_width-distanceBetweenPipes:
        pipes += [screen_width]
        pHole += [genHole()]

    if pipes[0] < -40:
        pipes.pop(0)
        pHole.pop(0)
    pHoleOBJ = []
    pipesOBJ = []
    for ind, i in enumerate(pipes):
        pipes[ind] -= speed
        pipesOBJ += [list(makePipes(i, ind))]
        #pHoleOBJ += [pg.draw.rect(screen, (0, 0, 0), [pipes[ind],pHole[ind],20,holeSize])]

    ## MOVE PLAYER
    startX = screen_width - currentX - 10
    startY = screen_height - currentY - 10
    playerSprite.move(startX, startY)
    screen.blit(playerSprite.image, playerSprite.rect)

    ## HIT DETECTION
    for x in pipesOBJ: # Loops throug pipes
        if currentX == x[0].left: # Checks if the left most point of the pipe has the same x value as the player
            sc + 1 # Adds one point to the score

        if any([playerSprite.rect.colliderect(x[ind]) for ind, _ in enumerate(x)]):
            print("Player hit pipe")
            dead()
            going = False
            break

    ## wait till next frame
    time.sleep(1/fps)
    sc.update()
    pg.display.update()