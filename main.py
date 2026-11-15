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

smallFont = pygame.font.Font(("Kalam-Regular.ttf"), 30)
TaskFont = pygame.font.Font(("Kalam-Regular.ttf"), 50)
GameOverWinFont = pygame.font.Font(("Kalam-Regular.ttf"), 90)
StartFont = pygame.font.Font(("Kalam-Regular.ttf"), 90)
BigStartFont = pygame.font.Font(("Kalam-Regular.ttf"), 120)

background = pygame.image.load("imgs/background.png").convert_alpha()
background = pygame.transform.scale(background, (900, 900))

catpicture = pygame.image.load("imgs/cat.png").convert_alpha()
catpicture = pygame.transform.scale(catpicture, (200, 200))

#Dialogue stuff starts here
MonsterGuy = pygame.image.load("dialogueimgs/Monster1Frame1.png").convert_alpha()
MonsterGuy = pygame.transform.scale(MonsterGuy, (500, 500))

BossGuy = pygame.image.load("dialogueimgs/Boss.png").convert_alpha()
BossGuy = pygame.transform.scale(BossGuy, (600, 600))

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

enemy = Hitman(700, 350, EnemySpriteLeft, EnemySpriteRight)
enemy.facing = -1

ENEMYHEALTHBAR_X = enemy.rect.x
ENEMYHEALTHBAR_Y = enemy.rect.y
ENEMYHEALTHBAR_HEIGHT = 25
ENEMYHEALTHBAR_CURRENT_WIDTH = 100

EnemyHealthbar = pygame.Rect(ENEMYHEALTHBAR_X, ENEMYHEALTHBAR_Y, ENEMYHEALTHBAR_CURRENT_WIDTH, ENEMYHEALTHBAR_HEIGHT)

ENEMYBACKGROUNDHEALTHBARWIDTH = 100
EnemyBackgroundHealthbar = pygame.Rect(ENEMYHEALTHBAR_X, ENEMYHEALTHBAR_Y, ENEMYBACKGROUNDHEALTHBARWIDTH, ENEMYHEALTHBAR_HEIGHT)

EnemyHealth = 100

EnemyBulletSprite = pygame.image.load("imgs/Bullet.png").convert_alpha()
EnemyBulletSprite = pygame.transform.scale(EnemyBulletSprite, (15, 15))
enemybullet = Bullet(EnemyBulletSprite)

EnemyRaycast = pygame.rect.Rect(enemy.rect.x, enemy.rect.y, 200, 100) # raycast for the ai system

CurrentMode = "Dialogue1"
GameRunning = True
while GameRunning:
    CurrentTime = pygame.time.get_ticks()

    TestWave = math.sin(CurrentTime * 0.005) * 10
    clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameRunning = False
            break
        keys = pygame.key.get_pressed()
        mouseposition = pygame.mouse.get_pos()

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

        if keys[pygame.K_ESCAPE]:
            CurrentMode = "Start"

        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
            if not playerbullet.active:
                if hitman.facing == 1:
                    direction = 1 # changes bullet trajectory on player direction
                if hitman.facing == -1:
                    direction = -1
                playerbullet.fire(hitman.rect.x + 40, hitman.rect.y + 50, direction)

    if CurrentMode == "Playing":
        playerbullet.update() # updates player bullet every tick
        enemybullet.update() # updates enemy bullet every tick
        hitman.update() # updates player every tick
        enemy.update() # updates enemy every tick

        if hitman.rect.x < enemy.rect.x:
            enemy.facing = -1
            EnemyRaycast.topleft=(enemy.rect.x - 300, enemy.rect.y)

        if hitman.rect.x > enemy.rect.x:
            enemy.facing = 1
            EnemyRaycast.topleft=(enemy.rect.x + 100, enemy.rect.y)

        elif hitman.jumping:
            enemy.jumping = True

        WithinRange = EnemyRaycast.colliderect(hitman.rect)

        if WithinRange:
            enemy.vel_x = 0
        else:
            enemy.vel_x = 2 * enemy.facing

        if enemybullet.active == False:
            direction = -1 if enemy.facing == -1 else 1
            enemybullet.fire(enemy.rect.x + 40, enemy.rect.y + 50, direction)

        if enemybullet.active:
            if enemybullet.rect.colliderect(hitman.rect):
                enemybullet.active = False
                PlayerHealth -= 10
                Healthbar.width += -20
        if playerbullet.active:
            if playerbullet.rect.colliderect(enemy.rect):
                playerbullet.active = False
                EnemyHealthbar.width += -20
                EnemyHealth -= 20

        if PlayerHealth > 60:
            EnemyRaycast = pygame.rect.Rect(enemy.rect.x, enemy.rect.y, 100, 100)

        if PlayerHealth <= 0:
            CurrentMode = "Loss"

        if EnemyHealth <= 0:
            CurrentMode = "Win"

    window.fill((0, 0, 0))

    if GameRunning:
        if CurrentMode == "Playing":
            window.blit(background, (0, -200))
            TaskText = TaskFont.render("Mission: Kill the organization spy..", True, (255, 255, 255))
            window.blit(TaskText, (50, 50 + TestWave))
            Healthbar.topleft=(hitman.rect.x - 50, hitman.rect.y - 100 + TestWave)
            BackgroundHealthbar.topleft=(hitman.rect.x - 50, hitman.rect.y - 100 + TestWave)
            EnemyHealthbar.topleft=(enemy.rect.x + 5, enemy.rect.y - 25 + TestWave)
            EnemyBackgroundHealthbar.topleft=(enemy.rect.x + 5, enemy.rect.y - 25 + TestWave)
            
            pygame.draw.rect(window, (200, 0, 0), EnemyBackgroundHealthbar)
            pygame.draw.rect(window, (135, 249, 89), EnemyHealthbar)

            pygame.draw.rect(window, (200, 0, 0), BackgroundHealthbar)
            pygame.draw.rect(window, (135, 249, 89), Healthbar)
            enemybullet.draw(window)
            playerbullet.draw(window)
            hitman.draw(window)
            enemy.draw(window)

        if CurrentMode == "Loss":
            window.fill((153, 0, 0))
            FirstGameOvertext = GameOverWinFont.render("The Organization", True, (255, 255, 255))
            SecondGameOvertext = GameOverWinFont.render("succeeded..", True, (255, 255, 255))
            EnemySpriteLeft = pygame.transform.scale(EnemySpriteLeft, (500, 500))
            hitman = Hitman(-100, 1000, PlayerFrameLeft, PlayerFrameRight)
            window.blit(FirstGameOvertext, (50, 50))
            window.blit(SecondGameOvertext, (100, 140))
            window.blit(EnemySpriteLeft, (500, 200))
        if CurrentMode == "Win":
            window.fill((135, 249, 89))
            FirstWinText = GameOverWinFont.render("You reppelled the", True, (255, 255, 255))
            SecondWinText = GameOverWinFont.render("Organization..", True, (255, 255, 255))
            PlayerFrameLeft = pygame.transform.scale(PlayerFrameLeft, (500, 500))
            hitman = Hitman(-100, 1000, PlayerFrameLeft, PlayerFrameRight)
            window.blit(FirstWinText, (50, 50))
            window.blit(SecondWinText, (100, 140))
            window.blit(PlayerFrameLeft, (500, 200))

        if CurrentMode == "Start":
            window.fill((0, 0, 0))
            SmallStartText = StartFont.render("-Start-", True, (255, 255, 255))
            BigStartText = BigStartFont.render("-Start-", True, (255, 255, 255))
            startbuttonrect = SmallStartText.get_rect(topleft=(50, 200))
            SmallCreditText = StartFont.render("-Credits-", True, (255, 255, 255))
            BigCreditsText = BigStartFont.render("-Credits-", True, (255, 255, 255))
            creditbuttonrect = SmallCreditText.get_rect(topleft=(50, 400))
            if startbuttonrect.collidepoint(mouseposition):
                window.blit(BigStartText, startbuttonrect)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    CurrentMode = "Playing"
            else:
                window.blit(SmallStartText, startbuttonrect)
            if creditbuttonrect.collidepoint(mouseposition):
                window.blit(BigCreditsText, creditbuttonrect)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    CurrentMode = "Credits"
            else:
                window.blit(SmallCreditText, creditbuttonrect)
        if CurrentMode == "Credits":
            window.fill((0, 0, 0))
            GameCreditstext = smallFont.render("Game Design: Seaw33", True, (255, 255, 255))
            DevCreditstext = smallFont.render("Main Dev: Seaw33", True, (255, 255, 255))
            SubDevCreditstext = smallFont.render("Sub Dev: Seaw33", True, (255, 255, 255))
            AllCreditstext = smallFont.render("Litterally everything: Seaw33", True, (255, 255, 255))
            BackButton = StartFont.render("Back", True, (255, 255, 255))
            BigBackButton = BigStartFont.render("Back", True, (255, 255, 255))
            BackbuttonRect = BackButton.get_rect(topleft=(400, 400))
            window.blit(GameCreditstext, (100, 50 + TestWave))
            window.blit(DevCreditstext, (100, 120 + TestWave))
            window.blit(SubDevCreditstext, (100, 190 + TestWave))
            window.blit(AllCreditstext, (100, 260 + TestWave))
            if BackbuttonRect.collidepoint(mouseposition):
                window.blit(BigBackButton, BackbuttonRect)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    CurrentMode = "Start"
            else:
                window.blit(BackButton, BackbuttonRect)

        if CurrentMode == "Dialogue1":
            window.fill((0, 0, 0))
            window.blit(MonsterGuy, (400, -50 + TestWave))
            window.blit(PlayerFrameRight, (200, 200))
            Dialogue1 = TaskFont.render("After the defeat of the monster..", True, (255, 255, 255))
            ClicktoSkip1 = smallFont.render("Click to continue..", True, (255, 255, 255))
            ContinueRect1 = Dialogue1.get_rect(topleft=(100,400))
            window.blit(Dialogue1, ContinueRect1)
            window.blit(ClicktoSkip1, (300, 470))
            if clicked:
                if ContinueRect1.collidepoint(mouseposition):
                    CurrentMode = "Dialogue2"
        elif CurrentMode == "Dialogue2":
            window.fill((25, 0, 0))
            window.blit(BossGuy, (300, 100))
            Dialogue2 = TaskFont.render("The organization was angered..", True, (255, 255, 255))
            ClicktoSkip2 = smallFont.render("Click to continue..", True, (255, 255, 255))
            ContinueRect2 = Dialogue2.get_rect(topleft=(150,400))
            window.blit(Dialogue2, ContinueRect2)
            window.blit(ClicktoSkip2, (300, 470))
            if clicked:
                if ContinueRect2.collidepoint(mouseposition):
                    CurrentMode = "Dialogue3"
        elif CurrentMode == "Dialogue3":
            window.fill((0, 0, 0))
            EnemySpriteLeft = pygame.transform.scale(EnemySpriteLeft, (600, 600))
            window.blit(EnemySpriteLeft, (500, 150))
            Dialogue3 = TaskFont.render("They had sent one of their hitmen.", True, (255, 255, 255))
            ClicktoSkip3 = smallFont.render("Click to continue..", True, (255, 255, 255))
            ContinueRect3 = Dialogue3.get_rect(topleft=(75,400))
            window.blit(Dialogue3, ContinueRect3)
            window.blit(ClicktoSkip3, (300, 470))
            if clicked:
                if ContinueRect3.collidepoint(mouseposition):
                    CurrentMode = "Dialogue4"
        elif CurrentMode == "Dialogue4":
            window.fill((20, 20, 20))
            PlayerFrameRight = pygame.transform.scale(PlayerFrameRight, (600, 600))
            window.blit(PlayerFrameRight, (-200, 150))
            Dialogue4 = TaskFont.render("And I dont even know why..", True, (255, 255, 255))
            ClicktoSkip4 = smallFont.render("Click to continue..", True, (255, 255, 255))
            ContinueRect4 = Dialogue4.get_rect(topleft=(100, 50))
            window.blit(Dialogue4, ContinueRect4)
            window.blit(ClicktoSkip4, (400, 120))
            if clicked:
                if ContinueRect4.collidepoint(mouseposition):
                    CurrentMode = "Start"

    pygame.display.flip()
    clock.tick(60)