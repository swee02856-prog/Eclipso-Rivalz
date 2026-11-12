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

PLAYERX = 200
PLAYERY = 350
PLAYERVELX = 0
PLAYERVELY = 0

playerside = PlayerFrameRight

# Player jumping
Y_GRAVITY = 1
JUMP_HEIGHT = 20
Y_VELOCITY = JUMP_HEIGHT
jumping = False

# Enemy Jumping
ENEMY_Y_GRAVITY = 1
ENEMY_JUMP_HEIGHT = 20
ENEMY_Y_VELOCITY = ENEMY_JUMP_HEIGHT
EnemyJump = False

bulletsprite = pygame.image.load("imgs/Bullet.png").convert_alpha()
bulletsprite = pygame.transform.scale(bulletsprite, (15, 15))
bulletshot = False

BULLETX = 0
BULLETY = 0
BULLETVELX = 0
BULLETVELY = 0

EnemySpriteLeft = pygame.image.load("imgs/EnemySpriteLeft.png").convert_alpha()
EnemySpriteLeft = pygame.transform.scale(EnemySpriteLeft, (100, 100))
EnemySpriteRight = pygame.image.load("imgs/EnemySpriteRight.png").convert_alpha()
EnemySpriteRight = pygame.transform.scale(EnemySpriteRight, (100, 100))

Enemyside = EnemySpriteLeft

ENEMY_X = 700
ENEMY_Y = 350
ENEMY_VEL_X = 0
ENEMY_VEL_Y = 0

EnemyHitbox = pygame.rect.Rect(ENEMY_X, ENEMY_Y, 100, 100)

EnemyBulletSprite = pygame.image.load("imgs/Bullet.png").convert_alpha()
EnemyBulletSprite = pygame.transform.scale(EnemyBulletSprite, (15, 15))
EnemyBulletShot = False

BulletHitbox = pygame.rect.Rect(BULLETX, BULLETY, 15, 15)

ENEMYBULLETX = 0
ENEMYBULLETY = 0
ENEMYBULLET_VEL_X = 0
ENEMYBULLET_VEL_Y = 0

EnemyBulletHitbox = pygame.rect.Rect(ENEMYBULLETX, ENEMYBULLETY, 15, 15)

EnemyRaycast = pygame.rect.Rect(ENEMY_X, ENEMY_Y, 300, 100)
PlayerHitbox = pygame.rect.Rect(PLAYERX, PLAYERY, 80, 80)

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
        PLAYERY -= Y_VELOCITY
        Y_VELOCITY -= Y_GRAVITY
        if Y_VELOCITY < -JUMP_HEIGHT:
            Y_VELOCITY = JUMP_HEIGHT
            jumping = False

    if EnemyJump:
        ENEMY_Y -= ENEMY_Y_VELOCITY
        ENEMY_Y_VELOCITY -= ENEMY_Y_GRAVITY
        if ENEMY_Y_VELOCITY < -ENEMY_JUMP_HEIGHT:
            ENEMY_Y_VELOCITY = ENEMY_JUMP_HEIGHT
            EnemyJump = False

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

    ENEMY_X += ENEMY_VEL_X
    ENEMY_Y += ENEMY_VEL_Y

    PlayerHitbox.topleft=(PLAYERX, PLAYERY)
    EnemyHitbox.topleft=(ENEMY_X, ENEMY_Y)
    BulletHitbox.topleft=(BULLETX, BULLETY)
    EnemyBulletHitbox.topleft=(ENEMYBULLETX, ENEMYBULLETY)

    if bulletshot == False:
        BULLETX = PLAYERX + 40
        BULLETY = PLAYERY + 50
    BULLETX += BULLETVELX

    if EnemyBulletShot == False:
        ENEMYBULLETX = ENEMY_X + 40
        ENEMYBULLETY = ENEMY_Y + 50
    ENEMYBULLETX += ENEMYBULLET_VEL_X

    if PLAYERX < ENEMY_X:
        Enemyside = EnemySpriteLeft
        EnemyRaycast.topleft=(ENEMY_X - 300, ENEMY_Y)

    if PLAYERX > ENEMY_X:
        Enemyside = EnemySpriteRight
        EnemyRaycast.topleft=(ENEMY_X + 100, ENEMY_Y)

    elif jumping:
        EnemyJump = True

    else:
        ENEMY_VEL_X = 0
        ENEMY_VEL_Y = 0

    if EnemyRaycast.colliderect(PlayerHitbox):
        print("Player in range")

    window.fill((0, 0, 0))

    if GameRunning:
        window.blit(EnemyBulletSprite, (ENEMYBULLETX, ENEMYBULLETY))
        window.blit(Enemyside, (ENEMY_X, ENEMY_Y))
        window.blit(bulletsprite, (BULLETX, BULLETY))
        window.blit(playerside, (PLAYERX, PLAYERY))

    pygame.display.flip()
    clock.tick(60)