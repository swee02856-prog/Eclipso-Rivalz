import pygame
import math
pygame.init()

clock = pygame.time.Clock()

window = pygame.display.set_mode((900, 600))
window.fill((0, 0, 0))
pygame.display.set_caption("Eclipso Rivalz")

PlayerFrameLeft = pygame.image.load("imgs/PlayerSpriteLeft.png").convert_alpha()
PlayerFrameLeft = pygame.transform.scale(PlayerFrameLeft, (100, 100))
PlayerFrameRight = pygame.image.load("imgs/PlayerSpriteRight.png").convert_alpha()
PlayerFrameRight = pygame.transform.scale(PlayerFrameRight, (100, 100))

PLAYERX = 300
PLAYERY = 350
PLAYERVELX = 0
PLAYERVELY = 0

playerside = PlayerFrameRight

Y_GRAVITY = 1
JUMP_HEIGHT = 20
Y_VEOCITY = JUMP_HEIGHT
jumping = False

bulletsprite = pygame.image.load("imgs/Bullet.png").convert_alpha()
bulletsprite = pygame.transform.scale(bulletsprite, (15, 15))
bulletshot = False
bulletsFired = 0

BULLETX = 0
BULLETY = 0
BULLETVELX = 0
BULLETVELY = 0

GameRunning = True
while GameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameRunning = False
            break
    
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            PLAYERVELX = 5
            playerside = PlayerFrameRight
        elif keys[pygame.K_a]:
            PLAYERVELX = -5
            playerside = PlayerFrameLeft
        else:
            PLAYERVELX = 0

        if keys[pygame.K_SPACE]:
            jumping = True
        if keys[pygame.K_w]:
            jumping = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if BULLETX == PLAYERX + 40 and bulletshot == False:
                bulletshot = True
                if playerside == PlayerFrameRight:
                    BULLETVELX = 10
                if playerside == PlayerFrameLeft:
                    BULLETVELX = -10

    if jumping:
        PLAYERY -= Y_VEOCITY
        Y_VEOCITY -= Y_GRAVITY
        if Y_VEOCITY < -JUMP_HEIGHT:
            Y_VEOCITY = JUMP_HEIGHT
            jumping = False

    if PLAYERX > 700:
        PLAYERX = 700
    if PLAYERX < 50:
        PLAYERX = 50

    if BULLETX > 900:
        bulletshot = False
        BULLETVELX = 0
    if BULLETX < 0:
        bulletshot = False
        BULLETVELX = 0

    PLAYERX += PLAYERVELX
    PLAYERY += PLAYERVELY

    if bulletshot == False:
        BULLETX = PLAYERX + 40
        BULLETY = PLAYERY + 50
    BULLETX += BULLETVELX

    window.fill((0, 0, 0))
    window.blit(bulletsprite, (BULLETX, BULLETY))
    window.blit(playerside, (PLAYERX, PLAYERY))

    pygame.display.flip()
    clock.tick(60)