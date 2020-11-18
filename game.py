import pygame as pg
import random
import time
import math

pg.init()

pg.display.init()

screen_width=800
screen_height=400

screen=pg.display.set_mode([screen_width, screen_height])

pg.key.set_repeat(500, 30)

fps = 75

currentY = screen_height/2
currentX = screen_width/2

debug = True # Set this to True to disable hit detection

grav = True
velY = 0
Max = 20 
holeSize = 150
speed = 2
thiccnessMultiplier = 2
pipeWideness = 40
pipeHeight = 40
distanceBetweenPipes = 200

pg.display.update()

genHole = lambda: random.randint(10, screen_height-(holeSize+10))

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
        Font = pg.font.Font('freesansbold.ttf', 32)
        text = Font.render(f'{self.score}', True, (116, 114, 158))
        rect = text.get_rect()
        rect.center = (10, screen_height-26)
        screen.blit(text, rect)

def dead():
    pg.font.init()
    Font = pg.font.Font('freesansbold.ttf', 32)
    text = Font.render('Game over', True, (116, 114, 158))
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
        time.sleep(1/fps)

class Player(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, picture="player.png"):
        super().__init__()
        self.Y = 0
        self.velY = 0
        self.image = pg.image.load(picture)
        self.image = pg.transform.smoothscale(self.image, (20*thiccnessMultiplier,30))

        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)

        screen.blit(self.image, self.rect)
    def gravity(self):
        '''
        run this every frame to aply gravity
        '''
        self.rect.y -= self.velY
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
        elif self.rect.top < 0:
            self.rect.top = 0
            self.velY = -1
        if self.velY > -10 and self.rect.y > 0:
            self.velY -= 0.5
        if self.rect.bottom < 0:
            self.velY = 0
        #print(self.velY)
        # print(currentY)
        screen.blit(self.image, self.rect)
        return self.rect
    def fly(self):
        self.velY += (Max-self.velY)*0.5
        print(self.velY)
        if self.velY > Max:
            self.velY = Max
    screen.fill((0,0,0))

playerSprite = Player(screen_width//2, screen_height//2)
playerGroup = pg.sprite.Group()
playerGroup.add(playerSprite)

class Pipe(pg.sprite.Sprite):
    def __init__(self, rect, isTop = False, flipped=False):
        self.isTop = isTop
        self.rect = pg.Rect(rect)
        if not self.isTop:
            self.image = pg.transform.smoothscale(pg.image.load("Pipe Bottom.png"), (self.rect.width, self.rect.height))
            self.width = self.rect.width
        else:
            self.image = pg.transform.smoothscale(pg.image.load("Pipe Top.png"), (self.rect.width, self.rect.height))
            if flipped:
                self.image = pg.transform.flip(self.image, False, True)
            self.width = self.rect.width
    def update(self, x):
        self.rect.x = self.rect.x - x
        screen.blit(self.image, self.rect)


class Pipes:
    def __init__(self, x=screen_width-40):
        self.pHole = genHole()
        self.x = x
        self.pipes = []
        self.pipes += [Pipe([x, 0, pipeWideness, self.pHole])]

        self.pipes += [Pipe([x, self.pHole+holeSize, pipeWideness, screen_height])]

        self.pipes += [Pipe([x, self.pHole-1, pipeWideness, 20], isTop=True, flipped=True)]

        self.pipes += [Pipe([x, self.pHole+holeSize, pipeWideness, 20],isTop=True)]

    def move(self, x, rect):
        global playerSprite
        '''
        pass how many pixel you want to move the pipe along the x axis
        '''
        for _, p in enumerate(self.pipes):
            p.update(x)
            dist = distanceBetweenPipes//4
            if not debug:
                if rect.colliderect(p.rect):
                    yield True
    def isAtEdge(self):
        return self.pipes[-1].rect.x <= 0
    def __left__(self):
        return self.pipes[-1].rect.x
    def reset(self):
        self.pHole = genHole()
        self.pipes = []
        self.pipes += [Pipe([self.x, 0, pipeWideness, self.pHole])]

        self.pipes += [Pipe([self.x, self.pHole+holeSize, pipeWideness, screen_height])]

        self.pipes += [Pipe([self.x, self.pHole-1, pipeWideness, pipeHeight], isTop=True, flipped=True)]

        self.pipes += [Pipe([self.x, self.pHole+holeSize, pipeWideness, pipeHeight],isTop=True)]

class PipeHandler:
    def __init__(self, amount=math.ceil(screen_width/distanceBetweenPipes)):
        self.pipes = [Pipes()]
        self.amount = amount + 1
        self.waiting = []
    def update(self, rect):
        for i in self.pipes:
            if i:
                if i.isAtEdge() and not i in self.waiting:
                    print("Attempting to reset pipe")
                    self.waiting += [i]
                else:
                    yield i.move(1, rect)
        try:
            if len(self.pipes) > 0:
                if self.pipes[-1].__left__() < screen_width-distanceBetweenPipes: 
                    if len(self.pipes) < self.amount:
                        print(f"making new pipe {self.pipes[-1].__left__()}")
                        self.pipes += [Pipes()]
                    elif len(self.waiting) > 0:
                        try:
                            self.pipes.remove(self.waiting[0])
                            self.waiting[0].reset()
                            self.pipes += self.waiting[0]
                            self.waiting.pip(0)
                        except Exception as e:
                            print(e)
        except:
            pass

class Background:
    def __init__(self, image, x, end):
        self.image = image
        self.end = end
        self.x = x
        self.y = 0
        self.rect = pg.Rect((self.x, self.y, screen_width, screen_height))
        self.default = self.x
    
    def update(self, x = 1, y = 0):
        self.x += x
        self.y += y
        if self.x >= self.end:
            self.x = self.default 
        self.rect = pg.Rect((self.x, self.y, screen_width, screen_height))

    def __reset__(self):
        self.image = self.default


class BackgroundHandler:
    def __init__(self, background="Background.jpg"):
        self.background = pg.transform.smoothscale(pg.image.load(background), (screen_width, screen_height))
        self.activeImage = Background(self.background, 0, screen_width)
        self.nonActive = Background(self.background, screen_width*-1, 0)
    def update(self):
        self.activeImage.update()
        self.nonActive.update()
        screen.blit(self.activeImage.image, self.activeImage.rect)
        screen.blit(self.nonActive.image, self.nonActive.rect)

clock = pg.time.Clock()

player = Player(currentX, currentY)

pg.display.update()

handler = PipeHandler()

# backgroundRect = pg.Rect((0, 0, screen_width, screen_height))
# backgroundImage = pg.transform.smoothscale(pg.image.load("Background.jpg"), (screen_width, screen_height))

background = BackgroundHandler()

while True:
    #screen.blit(backgroundImage, backgroundRect)
    background.update()
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.fly()
    pos = player.gravity()
    checkList = list(handler.update(pos))
    if any([any(i) for i in checkList]):
        dead()
        break
    time.sleep(1/fps)
    pg.display.update()