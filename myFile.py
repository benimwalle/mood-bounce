import pygame, sys
import random
import threading
import math
from pygame.locals import *
pygame.font.init()
myfont = pygame.font.SysFont('Impact', 30)
menu_font = pygame.font.Font(None, 40)
gameOverFont = pygame.font.SysFont('Impact', 200)

# Game State Constants
MAIN_MENU = 0
PAUSE = 1
LEVEL_ONE = 101
LEVEL_ONE_TRANSITION = 1015
LEVEL_TWO = 102
LEVEL_TWO_TRANSITION = 1025
LEVEL_THREE = 103
LEVEL_THREE_TRANSITION = 1035
LEVEL_FOUR = 104

END_GAME = 9
# QUIT = 999


def controlHealth():
    dead = 0
    if userBall.rect.collidelist(BallsRect)> -1:
        if not userBall.invincible:
            userBall.loseHealth()
            userBall.invincible = 1
    else:
        if userBall.invincible:
            userBall.invincible = 0
    if userBall.health == 0:
        dead = 1
    return dead


# Controls the Computer Balls
def controlBalls():
    for ball in Balls:
        ball.bounceOffWalls()
        if level == 1:
            # ball.change_mox(ball.mox+random.randint(-1,3))
            # ball.change_moy(ball.moy+random.randint(-1,3))
            ball.move()
        if level == 2:
            ball.move()
        if level == 3:
            ball.move()
        if level == 4:
            ball.move()

        DISPLAYSURF.blit(ball.currentImage, (ball.x, ball.y))


# User Health and Movement
def controlUser():
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        userBall.x -= USERSPEED
        userBall.rect.move_ip(-USERSPEED, 0)
        if userBall.x < 0:
            userBall.x = 0
            userBall.rect.move_ip(USERSPEED,0)
    if keys[K_RIGHT]:
        userBall.x += USERSPEED
        userBall.rect.move_ip(USERSPEED, 0)
        if userBall.x > width-125:
            userBall.x = width-125
            userBall.rect.move_ip(-USERSPEED,0)
    if keys[K_DOWN]:
        userBall.y += USERSPEED
        userBall.rect.move_ip(0,USERSPEED)
        if userBall.y > height-125:
            userBall.y = height-125
            userBall.rect.move_ip(0, -USERSPEED)
    if keys[K_UP]:
        userBall.y -= USERSPEED
        userBall.rect.move_ip(0, -USERSPEED)
        if userBall.y < 0:
            userBall.y = 0
            userBall.rect.move_ip(0,USERSPEED)
    if keys[K_SPACE]:
        if userBall.currentImage == userHappyImg:
            userBall.currentImage = userMedImg
        elif userBall.currentImage == userMedImg:
            userBall.currentImage =userSadImg
        elif userBall.currentImage ==userSadImg:
            userBall.currentImage = userDeadImg
        else:
            userBall.currentImage = userHappyImg
    DISPLAYSURF.blit(userBall.currentImage, (userBall.x, userBall.y))
    dead = controlHealth()
    return dead


# Helper Functions for ROTATE FACE. In use for computer whatever
def makeHappy():
    return [happyImg, 0]


def makeMedium():
    return [medImg, 1]


def makeSad():
    return [sadImg, 2]
# ###################################################################


class Ball(object):
    imgID = 0
    currentImage = ''
    x=0
    y=0
    mox = 0
    moy = 0
    rect = None
    max_speed = 5

    def __init__(self, imgID, currentImage, x, y, mox, moy, max_speed):
        self.imgID = imgID
        self.currentImage = currentImage
        self.x = x
        self.y = y
        self.mox = mox
        self.moy = moy
        self.max_speed = max_speed
        self.rect = pygame.Rect(self.x, self.y, 185, 185)

    def change_mox(self, new_mox):
        if abs(new_mox) < self.max_speed:
            self.mox = new_mox
        else: #You're trying to set the x speed to higher than the max speed. set it to the max speed
            pass

    def change_moy(self, new_moy):
        if abs(new_moy) < self.max_speed:
            self.moy = new_moy
        else: # You're trying to set the y speed to higher than the max speed. set it to the max speed
            pass
            # if new_moy > 0:
                # self.moy = self.max_speed
            # else:
                # self.moy = -self.max_speed


    def rotateFace(self):
        if self.imgID == 0:
            self.currentImage = makeMedium()[0]
            self.imgID = makeMedium()[1]
        elif self.imgID == 1:
            self.currentImage = makeSad()[0]
            self.imgID = makeSad()[1]
        elif self.imgID == 2:
            self.currentImage = makeHappy()[0]
            self.imgID = makeHappy()[1]


    def reverseX(self):
        self.mox = -self.mox

    def reverseY(self):
        self.moy = -self.moy

    def move(self):
        self.x += self.mox
        self.y += self.moy
        self.rect.move_ip(self.mox, self.moy)

    def bounceOffWalls(self):
        bounced = 0
        if self.x <= 0:
            self.reverseX()
            bounced = 1
        if self.y <= 0:
            self.reverseY()
            bounced = 1
        if self.x >= width - 185:
            self.reverseX()
            bounced = 1
        if self.y >= height - 185:
            self.reverseY()
            bounced = 1
        if bounced:
            boingSound.play()
            self.rotateFace()


# Make the computer ball
def make_ball(imgID, currentImage, x, y, mox, moy, max_speed):
    ball = Ball(imgID, currentImage, x, y, mox, moy, max_speed)
    return ball


# add a computer ball to the screen and collision stuff. i is a seed
def add_ball(x, y, mox, moy, max):
    myBall = make_ball(0, happyImg, x, y, mox, moy, max)
    Balls.append(myBall)
    BallsRect.append(myBall.rect)


class userBall(object):
    x = 0
    y = 0
    invincible = 0
    health = 3
    currentImage = 'userHappy'
    rect = None

    def __init__(self):
        self.x = width-200
        self.y = height-200
        self.health = 3
        self.currentImage = userHappyImg
        self.rect = pygame.Rect(self.x, self.y, 125, 125)

    def reset(self):
        self.x = width-200
        self.y = height-200
        self.health = 3
        self.currentImage = userHappyImg
        self.rect = pygame.Rect(self.x, self.y, 125, 125)

    def loseHealth(self):
        if self.health == 3:
            DISPLAYSURF.fill(Color(255, 0, 0, 255))
            self.health = 2
            self.currentImage = userMedImg
        elif self.health == 2:
            DISPLAYSURF.fill(Color(255, 0, 0, 0))
            self.health = 1
            self.currentImage = userSadImg
        elif self.health == 1:
            DISPLAYSURF.fill(Color(255, 0, 0, 0))
            self.health = 0
            self.currentImage = userDeadImg

    def bounceComputerBall(self, Ball):
        pass

    def restore_all_health(self):
        self.health = 3
        self.currentImage = userHappyImg


def make_user_ball():
    user = userBall()
    return user


class Option:
    hovered = False

    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw()

    def draw(self):
        self.set_rend()
        DISPLAYSURF.blit(self.rend, self.rect)

    def set_rend(self):
        self.rend = menu_font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            return (255, 255, 255)
        else:
            return (0, 200,200)

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos


def drawMenu():
    for idx, option in enumerate(options):
        if option.rect.collidepoint(pygame.mouse.get_pos()):
            option.hovered = True
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            if event.type == pygame.MOUSEBUTTONUP:
                if idx == 0:
                    return 1
                elif idx == 1:
                    return 0
                elif idx == 2:
                    return 3
        else:
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
            option.hovered = False
        option.draw()
    return 2


def drawStartMenu():
    for idx, option in enumerate(startOptions):
        if option.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            option.hovered = True
            if event.type == pygame.MOUSEBUTTONUP:
                if idx == 0:
                    return 1
                if idx == 1:
                    return 2
        else:
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
            option.hovered = False
        option.draw()
    return 0


def draw_pause_menu():
    for idx, option in enumerate(pause_options):
        if option.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            option.hovered = True
            if event.type == pygame.MOUSEBUTTONUP:
                if idx == 0:
                    return 1
                if idx == 1:
                    return 2
                if idx == 2:
                    return 3
        else:
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
            option.hovered = False
        option.draw()
    return 0


pygame.init()
USERSPEED = 25
FPS = 30
fpsClock = pygame.time.Clock()
height = 900
width = 1500
DISPLAYSURF = pygame.display.set_mode((width,height),0,32)
pygame.display.set_caption('Mood Bounce')


happyImg = pygame.image.load('smily.png')
medImg = pygame.image.load('straight.png')
sadImg = pygame.image.load('sad.png')
userHappyImg = pygame.image.load('userHappy.png')
userMedImg = pygame.image.load('userMedium.png')
userSadImg = pygame.image.load('userSad.png')
userDeadImg = pygame.image.load('userDead.png')
boingSound = pygame.mixer.Sound('boing.wav')
boingSound.set_volume(0.1)

pygame.display.set_icon(userHappyImg)


def timer(startTime, pauseTime):
    currentTime = pygame.time.get_ticks()
    currentTime = currentTime - startTime - pauseTime
    currentTime = currentTime / 10
    textsurface = myfont.render(str(currentTime), True, (0, 200, 200))
    DISPLAYSURF.blit(textsurface, (1425, 0))
    return currentTime


def drawLevelScore():
    text_surface = myfont.render("Level: {0}".format(str(level)), True, (0,200,200))
    DISPLAYSURF.blit(text_surface, (1300,0))

def mainGame(startTime, pauseTime):
    controlBalls()
    dead = controlUser()
    time = timer(startTime, pauseTime)
    drawLevelScore()
    return {"dead": dead, "time": time}


def drawGameOver(time):
    textsurface = myfont.render(str(time), True, (0, 200, 200))
    gameOverSurface = gameOverFont.render("GAME OVER", True, (200,0,200))
    DISPLAYSURF.blit(textsurface, (1400, 0))
    DISPLAYSURF.blit(gameOverSurface, (300, 250))

def drawStart():
    startSurface = gameOverFont.render("Mood Bounce", True, (200,0,200))
    DISPLAYSURF.blit(startSurface, (200, 250))

startOptions = [Option("START GAME", (300,500)), Option("QUIT", (300, 550))]
options = [Option("PLAY AGAIN", (500, 505)), Option("MAIN MENU", (500, 545)), Option("QUIT", (500, 585))]
pause_options = [Option("RESUME", (500, 505)), Option("MAIN MENU", (500, 545)), Option("QUIT", (500, 585))]

initial_load = 1
initial_pause = 1
userBall = make_user_ball()
gameState = MAIN_MENU
level = 1

running = True
pause_time = 0
while running:
    keys = pygame.key.get_pressed()
    if keys[K_p]:
        if gameState != 1:
            prev_state = gameState
        gameState = PAUSE

    DISPLAYSURF.fill((0, 0, 0))

    if gameState == MAIN_MENU:
        startMenuSelection = drawStartMenu()
        drawStart()
        if startMenuSelection == 1:
            initial_load = 1
            gameState = LEVEL_ONE
        if startMenuSelection == 2:
            running = False
            continue

    if gameState == LEVEL_ONE:
        if initial_load:
            pygame.mouse.set_visible(False)
            startTime = pygame.time.get_ticks()
            Balls = []
            BallsRect = []
            userBall.reset()
            for i in range(0,3):
                add_ball((i*100)+150, (i*100)+150, (i*3)+3, (i*3)+3, 8)
            initial_load = 0
        stopGame = mainGame(startTime, pause_time)

        if stopGame["time"] > 2000:
            initial_load = 1
            gameState = LEVEL_ONE_TRANSITION

        if stopGame["dead"]:
            pygame.mouse.set_visible(True)
            gameState = END_GAME

    if gameState == LEVEL_ONE_TRANSITION:
        stopGame = mainGame(startTime, pause_time)
        if initial_load:
            BallsRect = []
            level = 2
            userBall.restore_all_health()
            initial_load = 0
        for ball in Balls:
            ball.currentImage = pygame.transform.scale(ball.currentImage, (ball.currentImage.get_height()-16,ball.currentImage.get_width()-16))
            # DISPLAYSURF.blit(ball.currentImage, (ball.x, ball.y))
            if ball.currentImage.get_width() <= 25:
                Balls = []
        if stopGame["time"] > 2500:
            initial_load = 1
            gameState = LEVEL_TWO
        # todo change background
        # todo change level

    if gameState == LEVEL_TWO:
        if initial_load:
            # create balls
            Balls = []
            BallsRect = []
            for i in range(0, 9):
                add_ball(((i%3)*300)+50, ((i/3)*200)+50, 5, 5 , 3)
            userBall.restore_all_health()
            initial_load = 0
        stopGame = mainGame(startTime, pause_time)

        if stopGame["time"] > 4500:
            initial_load = 1
            gameState = LEVEL_TWO_TRANSITION

        if stopGame["dead"]:
            pygame.mouse.set_visible(True)
            gameState = END_GAME

    elif gameState == LEVEL_TWO_TRANSITION:
        stopGame = mainGame(startTime, pause_time)
        if initial_load:
            BallsRect = []
            level = 3
            userBall.restore_all_health()
            initial_load = 0
        for ball in Balls:
            ball.currentImage = pygame.transform.scale(ball.currentImage, (ball.currentImage.get_height()-16,ball.currentImage.get_width()-16))
            # DISPLAYSURF.blit(ball.currentImage, (ball.x, ball.y))
            if ball.currentImage.get_width() <= 25:
                Balls = []
        if stopGame["time"] > 5000:
            initial_load = 1
            gameState = LEVEL_THREE
        # todo change background
        # todo change level

    elif gameState == LEVEL_THREE:
        if initial_load:
            Balls = []
            BallsRect = []
            add_ball(10,10,15,15,15)
            add_ball(width-200, 10, -15,15, 15)
            add_ball(10, height-200, 15,-15, 15)
            add_ball(width-200, height-200, -15,-15, 15)
            initial_load = 0
        stopGame = mainGame(startTime, pause_time)

        if stopGame["time"] > 7000:
            initial_load = 1
            gameState = LEVEL_THREE_TRANSITION

        if (stopGame["dead"]):
            pygame.mouse.set_visible(True)
            gameState = END_GAME

    elif gameState == LEVEL_THREE_TRANSITION:
        stopGame = mainGame(startTime, pause_time)
        if initial_load:
            BallsRect = []
            level = 4
            userBall.restore_all_health()
            initial_load = 0
        for ball in Balls:
            ball.currentImage = pygame.transform.scale(ball.currentImage, (ball.currentImage.get_height()-16,ball.currentImage.get_width()-16))
            #DISPLAYSURF.blit(ball.currentImage, (ball.x, ball.y))
            if ball.currentImage.get_width() <= 25:
                Balls = []
        if stopGame["time"] > 7500:
            initial_load = 1
            gameState = LEVEL_FOUR
        # todo change background
        # todo change level

    elif gameState == LEVEL_FOUR:
        if initial_load:
            Balls = []
            BallsRect = []
            add_ball(10, 10, 40, 15, 40)

            initial_load = 0
        stopGame = mainGame(startTime, pause_time)

        if stopGame["time"] > 100000:
            initial_load = 1
            gameState = END_GAME

        if (stopGame["dead"]):
            pygame.mouse.set_visible(True)
            gameState = END_GAME

    elif gameState == END_GAME:
        pygame.mouse.set_visible(True)
        drawGameOver(stopGame["time"])
        menuSelect = drawMenu()
        if menuSelect == 0:
            gameState = MAIN_MENU
        if menuSelect == 1:
            initial_load = 1
            level = 1
            gameState = LEVEL_ONE
        if menuSelect == 3:
            running = False
            continue

    elif gameState == PAUSE:
        # drawGameOver(stopGame["time"])
        if initial_pause:
            pause_time_start = pygame.time.get_ticks()
            print "start: {}".format(pause_time_start)
            pygame.mouse.set_visible(True)
            initial_pause = 0
        pause_menu_selection = draw_pause_menu()
        if pause_menu_selection == 1:
            pause_time_end = pygame.time.get_ticks()
            pause_time = pause_time + (pause_time_end - pause_time_start)
            pygame.mouse.set_visible(False)
            initial_pause = 1
            gameState = prev_state
        elif pause_menu_selection == 2:
            initial_pause = 1
            gameState = MAIN_MENU
        elif pause_menu_selection == 3:
            gameState = QUIT

    elif gameState == QUIT:
        running = False
        continue

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            pygame.display.quit()
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fpsClock.tick(FPS)



