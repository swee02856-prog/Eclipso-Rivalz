import pygame
import math
pygame.init()

clock = pygame.time.Clock()

class Hitman:
    def __init__(self, x, y, sprite_left, sprite_right):
        self.sprite_left = sprite_left
        self.sprite_right = sprite_right
        self.rect = pygame.Rect(x, y, 80, 80)
        self.vel_x = 0
        self.facing = 1
        self.jumping = False
        self.y_gravity = 1
        self.jump_height = 20
        self.y_velocity = self.jump_height
    def update(self):
        if self.jumping:
            self.rect.y -= self.y_velocity
            self.y_velocity -= self.y_gravity
            if self.y_velocity < -self.jump_height:
                self.y_velocity = self.jump_height
                self.jumping = False
        self.rect.x += self.vel_x
        if self.rect.x > 800:
            self.rect.x = 800
        if self.rect.x < 100:
            self.rect.x = 100
    def draw(self, window):
        sprite = self.sprite_right if self.facing == 1 else self.sprite_left
        window.blit(sprite, self.rect.topleft)

class Bullet:
    def __init__(self, sprite):
        self.sprite = sprite
        self.rect = pygame.Rect(0, 0, 15, 15)
        self.vel_x = 0
        self.active = False

    def fire(self, x, y, direction):
        self.rect.topleft = (x, y)
        self.vel_x = 10 * direction
        self.active = True

    def update(self):
        if self.active == True:    
            self.rect.x += self.vel_x
            if self.rect.x > 900:
                self.active = False
            if self.rect.x < 0:
                self.active = False

    def draw(self, window):
        if self.active:
            window.blit(self.sprite, self.rect)

window = pygame.display.set_mode((900, 600))
window.fill((0, 0, 0))
pygame.display.set_caption("Eclipso Rivalz")

TaskFont = pygame.font.Font(("Kalam-Regular.ttf"), 50)

# Player stuff starts here
PlayerFrameLeft = pygame.image.load("imgs/PlayerSpriteLeft.png").convert_alpha()
PlayerFrameLeft = pygame.transform.scale(PlayerFrameLeft, (100, 100))
PlayerFrameRight = pygame.image.load("imgs/PlayerSpriteRight.png").convert_alpha()
PlayerFrameRight = pygame.transform.scale(PlayerFrameRight, (100, 100))
hitman = Hitman(200, 350, PlayerFrameLeft, PlayerFrameRight)

PLAYERHEALTHBAR_X = hitman.rect.x
PLAYERHEALTHBAR_Y = hitman.rect.y
PLAYERHEALTHBAR_HEIGHT = 50
PLAYERHEALTHBAR_CURRENT_WIDTH = 200

Healthbar = pygame.Rect(PLAYERHEALTHBAR_X, PLAYERHEALTHBAR_Y, PLAYERHEALTHBAR_CURRENT_WIDTH, PLAYERHEALTHBAR_HEIGHT)

PLAYERBACKGROUNDHEALTHBARWIDTH = 200
BackgroundHealthbar = pygame.Rect(PLAYERHEALTHBAR_X, PLAYERHEALTHBAR_Y, PLAYERBACKGROUNDHEALTHBARWIDTH, PLAYERHEALTHBAR_HEIGHT)

PlayerHealth = 100
# Player stuff ends here

# Enemy Jumping
ENEMY_Y_GRAVITY = 1
ENEMY_JUMP_HEIGHT = 20
ENEMY_Y_VELOCITY = ENEMY_JUMP_HEIGHT
EnemyJump = False

bulletsprite = pygame.image.load("imgs/Bullet.png").convert_alpha()
bulletsprite = pygame.transform.scale(bulletsprite, (15, 15))
playerbullet = Bullet(bulletsprite)

EnemySpriteLeft = pygame.image.load("imgs/EnemySpriteLeft.png").convert_alpha()
EnemySpriteLeft = pygame.transform.scale(EnemySpriteLeft, (100, 100))
EnemySpriteRight = pygame.image.load("imgs/EnemySpriteRight.png").convert_alpha()
EnemySpriteRight = pygame.transform.scale(EnemySpriteRight, (100, 100))

Enemyside = EnemySpriteLeft

ENEMY_X = 700
ENEMY_Y = 350
ENEMY_VEL_X = 0
ENEMY_VEL_Y = 0

ENEMYHEALTHBAR_X = ENEMY_X
ENEMYHEALTHBAR_Y = ENEMY_Y 
ENEMYHEALTHBAR_HEIGHT = 25
ENEMYHEALTHBAR_CURRENT_WIDTH = 100

EnemyHealthbar = pygame.Rect(ENEMYHEALTHBAR_X, ENEMYHEALTHBAR_Y, ENEMYHEALTHBAR_CURRENT_WIDTH, ENEMYHEALTHBAR_HEIGHT)

ENEMYBACKGROUNDHEALTHBARWIDTH = 100
EnemyBackgroundHealthbar = pygame.Rect(ENEMYHEALTHBAR_X, ENEMYHEALTHBAR_Y, ENEMYBACKGROUNDHEALTHBARWIDTH, ENEMYHEALTHBAR_HEIGHT)

EnemyHealth = 100

EnemyHitbox = pygame.rect.Rect(ENEMY_X, ENEMY_Y, 100, 100)

EnemyBulletSprite = pygame.image.load("imgs/Bullet.png").convert_alpha()
EnemyBulletSprite = pygame.transform.scale(EnemyBulletSprite, (15, 15))
enemybullet = Bullet(EnemyBulletSprite)

EnemyRaycast = pygame.rect.Rect(ENEMY_X, ENEMY_Y, 200, 100)
PlayerHitbox = pygame.rect.Rect(hitman.rect.x, hitman.rect.y, 80, 80)

GameRunning = True
while GameRunning:
    CurrentTime = pygame.time.get_ticks()

    TestWave = math.sin(CurrentTime * 0.005) * 10
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameRunning = False
            break
    
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            hitman.vel_x = 5
            hitman.facing = 1
        elif keys[pygame.K_a]:
            hitman.vel_x = -5
            hitman.facing = -1
        else:
            hitman.vel_x = 0

        if keys[pygame.K_SPACE]:
            hitman.jumping = True
        if keys[pygame.K_w]:
            hitman.jumping = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not playerbullet.active:
                if hitman.facing == 1:
                    direction = 1
                if hitman.facing == -1:
                    direction = -1
                playerbullet.fire(hitman.rect.x + 40, hitman.rect.y + 50, direction)

    if EnemyJump:
        ENEMY_Y -= ENEMY_Y_VELOCITY
        ENEMY_Y_VELOCITY -= ENEMY_Y_GRAVITY
        if ENEMY_Y_VELOCITY < -ENEMY_JUMP_HEIGHT:
            ENEMY_Y_VELOCITY = ENEMY_JUMP_HEIGHT
            EnemyJump = False

    if ENEMY_X > 700:
        ENEMY_X = 700
    if ENEMY_X < 100:
        ENEMY_X = 100

    playerbullet.update()
    hitman.update()

    ENEMY_X += ENEMY_VEL_X
    ENEMY_Y += ENEMY_VEL_Y
    enemybullet.update()

    PlayerHitbox.topleft=(hitman.rect.x, hitman.rect.y)
    EnemyHitbox.topleft=(ENEMY_X, ENEMY_Y)

    if hitman.rect.x < ENEMY_X:
        Enemyside = EnemySpriteLeft
        EnemyRaycast.topleft=(ENEMY_X - 300, ENEMY_Y)

    if hitman.rect.x > ENEMY_X:
        Enemyside = EnemySpriteRight
        EnemyRaycast.topleft=(ENEMY_X + 100, ENEMY_Y)

    elif hitman.jumping:
        EnemyJump = True

    else:
        ENEMY_VEL_X = 0
        ENEMY_VEL_Y = 0

    WithinRange = EnemyRaycast.colliderect(PlayerHitbox)

    if Enemyside == EnemySpriteLeft:
        if WithinRange:
            ENEMY_VEL_X = 0
        if WithinRange == False:
            ENEMY_VEL_X = -2

    if Enemyside == EnemySpriteRight:
        if WithinRange:
            ENEMY_VEL_X = 0
        if WithinRange == False:
            ENEMY_VEL_X = 2

    if enemybullet.active == False:
        direction = -1 if Enemyside == EnemySpriteLeft else 1
        enemybullet.fire(ENEMY_X + 40, ENEMY_Y + 50, direction)

    if enemybullet.active:
        if enemybullet.rect.colliderect(PlayerHitbox):
            enemybullet.active = False
            Healthbar.width += -20
    if playerbullet.active:
        if playerbullet.rect.colliderect(EnemyHitbox):
            playerbullet.active = False
            EnemyHealthbar.width += -10

    if PlayerHealth > 60:
        EnemyRaycast = pygame.rect.Rect(ENEMY_X, ENEMY_Y, 100, 100)

    window.fill((0, 0, 0))

    if GameRunning:
        TaskText = TaskFont.render("Mission: Kill the organization spy..", True, (255, 255, 255))
        window.blit(TaskText, (50, 50 + TestWave))
        Healthbar.topleft=(hitman.rect.x - 50, hitman.rect.y - 100 + TestWave)
        BackgroundHealthbar.topleft=(hitman.rect.x - 50, hitman.rect.y - 100 + TestWave)
        EnemyHealthbar.topleft=(ENEMY_X + 5, ENEMY_Y - 25 + TestWave)
        EnemyBackgroundHealthbar.topleft=(ENEMY_X + 5, ENEMY_Y - 25 + TestWave)
        
        pygame.draw.rect(window, (200, 0, 0), EnemyBackgroundHealthbar)
        pygame.draw.rect(window, (135, 249, 89), EnemyHealthbar)

        pygame.draw.rect(window, (200, 0, 0), BackgroundHealthbar)
        pygame.draw.rect(window, (135, 249, 89), Healthbar)
        enemybullet.draw(window)
        window.blit(Enemyside, (ENEMY_X, ENEMY_Y))
        playerbullet.draw(window)
        hitman.draw(window)

    pygame.display.flip()
    clock.tick(60)