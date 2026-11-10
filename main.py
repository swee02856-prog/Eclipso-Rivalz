import pygame
pygame.init()

clock = pygame.time.Clock()

window = pygame.display.set_mode((900, 600))
window.fill((0, 0, 0))
pygame.display.set_caption("Eclipso Rivalz")

PlayerFrameLeft = pygame.image.load("PlayerSpriteLeft.png").convert_alpha()
PlayerFrameLeft = pygame.transform.scale(PlayerFrameLeft, (100, 100))
PlayerFrameRight = pygame.image.load("PlayerSpriteRight.png").convert_alpha()
PlayerFrameRight = pygame.transform.scale(PlayerFrameRight, (100, 100))

PLAYERX = 0
PLAYERY = 0
PLAYERVELX = 0
PLAYERVELY = 0

playerside = PlayerFrameRight

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
        if keys[pygame.K_a]:
            PLAYERVELX = -5
            playerside = PlayerFrameLeft

    window.blit(playerside, (PLAYERX, PLAYERY))

    pygame.display.flip()
    clock.tick(60)