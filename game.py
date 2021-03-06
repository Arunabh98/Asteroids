import math
import random

import pygame
from pygame.locals import *

pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
keys = [False, False, False, False]
playerpos = [100, 100]
acc = [0, 0]
arrows = []
badtimer = 125
badtimer1 = 0
badguys = [[640, 100, 0]]
healthvalue = 194
pygame.mixer.init()

player = pygame.image.load("resources/images/spaceship1.png")
space = pygame.image.load("resources/images/space.jpg")
arrow = pygame.image.load("resources/images/bullet1.png")
badguyimg1 = pygame.image.load("resources/images/asteroid.png")
badguyimg = badguyimg1
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover1.png")
youwin = pygame.image.load("resources/images/youwin1.jpg")
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('resources/audio/moonlight.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

running = 1
exitcode = 0
while running:
    badtimer -= 1
    screen.fill(0)
    screen.blit(space, (0, 0))
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1] - (playerpos[1] + 32), position[0] - (playerpos[0] + 26))
    playerrot = pygame.transform.rotate(player, 360 - angle * 57.29)
    playerpos1 = (playerpos[0] - playerrot.get_rect().width / 2, playerpos[1] - playerrot.get_rect().height / 2)
    screen.blit(playerrot, playerpos1)
    for bullet in arrows:
        index = 0
        velx = math.cos(bullet[0]) * 3
        vely = math.sin(bullet[0]) * 3
        bullet[1] += velx
        bullet[2] += vely
        if bullet[1] < -64 or bullet[1] > 640 or bullet[2] < -64 or bullet[2] > 480:
            arrows.pop(index)
        index += 1
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360 - projectile[0] * 57.29)
            screen.blit(arrow1, (projectile[1], projectile[2]))
    if badtimer == 0:
        choice = random.choice(
            [[640, random.randint(50, 430), 0], [random.randint(50, 590), 450, 1], [0, random.randint(50, 430), 2],
             [640, random.randint(50, 430), 3], [0, random.randint(50, 430), 4], [random.randint(50, 590), 480, 5]])
        badguys.append(choice)
        print badguys[0]
        badtimer = 125 - (badtimer1 * 2)
        if badtimer1 >= 35:
            badtimer1 = 35
        else:
            badtimer1 += 5
    index = 0
    for badguy in badguys:
        if badguy[0] < -64:
            badguys.pop(index)
        if badguy[0] > 704:
            badguys.pop(index)
        if badguy[1] < -64:
            badguys.pop(index)
        if badguy[2] == 0:
            badguy[0] -= 2
        if badguy[2] == 1:
            badguy[1] -= 2
        if badguy[2] == 2:
            badguy[0] += 2
        if badguy[2] == 3:
            badguy[0] -= 2
            badguy[1] += 1
        if badguy[2] == 4:
            badguy[0] += 2
            badguy[1] -= 1
        if badguy[2] == 5:
            badguy[0] += 2
            badguy[1] -= 2
        spacerect = pygame.Rect(playerrot.get_rect())
        spacerect.top = playerpos1[1]
        spacerect.left = playerpos1[0]
        badrect = pygame.Rect(badguyimg.get_rect())
        badrect.top = badguy[1]
        badrect.left = badguy[0]
        if badrect.colliderect(spacerect):
            hit.play()
            healthvalue -= random.randint(15, 30)
            badguys.pop(index)
        index1 = 0
        for bullet in arrows:
            bullrect = pygame.Rect(arrow.get_rect())
            bullrect.left = bullet[1]
            bullrect.top = bullet[2]
            if badrect.colliderect(bullrect):
                enemy.play()
                acc[0] += 1
                badguys.pop(index)
                arrows.pop(index1)
            index1 += 1
        index += 1
    for badguy in badguys:
        screen.blit(badguyimg, (badguy[0], badguy[1]))
    font = pygame.font.Font(None, 24)
    survivedtext = font.render(
        str((90000 - pygame.time.get_ticks()) / 60000) + ":" + str((90000 - pygame.time.get_ticks()) / 1000 % 60).zfill(
            2), True, (255, 255, 0))
    textRect = survivedtext.get_rect()
    textRect.topright = [635, 5]
    screen.blit(survivedtext, textRect)
    screen.blit(healthbar, (5, 5))
    for health1 in range(healthvalue):
        screen.blit(health, (health1 + 8, 8))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN or event.type == MOUSEBUTTONDOWN:
            if event.type == MOUSEBUTTONDOWN:
                shoot.play()
                position = pygame.mouse.get_pos()
                acc[1] += 1
                arrows.append([math.atan2(position[1] - (playerpos1[1] + 32), position[0] - (playerpos1[0] + 26)),
                               playerpos1[0] + 32, playerpos1[1] + 32])
            keyp = pygame.key.get_pressed()
            if keyp[K_w]:
                keys[0] = True
            if keyp[K_a]:
                keys[1] = True
            if keyp[K_s]:
                keys[2] = True
            if keyp[K_d]:
                keys[3] = True
        if event.type == pygame.KEYUP:
            if event.key == K_w:
                keys[0] = False
            if event.key == K_a:
                keys[1] = False
            if event.key == K_s:
                keys[2] = False
            if event.key == K_d:
                keys[3] = False
    if keys[0]:
        playerpos[1] -= 2
        if playerpos[1] <= 0:
            playerpos[1] += 480
    if keys[2]:
        playerpos[1] += 2
        if playerpos[1] >= 480:
            playerpos[1] -= 480
    if keys[1]:
        playerpos[0] -= 2
        if playerpos[0] <= 0:
            playerpos[0] += 640
    if keys[3]:
        playerpos[0] += 2
        if playerpos[0] >= 640:
            playerpos[0] -= 640

    if pygame.time.get_ticks() >= 90000:
        running = 0
        exitcode = 1
    if healthvalue <= 0:
        running = 0
        exitcode = 0
    if acc[1] != 0:
        accuracy = acc[0] * 1.0 / acc[1] * 100
    else:
        accuracy = 0
if exitcode == 0:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: " + str(accuracy) + "%", True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 155
    screen.blit(gameover, (0, 0))
    screen.blit(text, textRect)
else:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: " + str(accuracy) + "%", True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 155
    screen.blit(youwin, (0, 0))
    screen.blit(text, textRect)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
