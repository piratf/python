# 1 - Import library
import pygame
import math
import random
import sys
from pygame.locals import *

__author__ = 'piratf'
__blog__ = 'http://piratf.github.io/'
# thank to Julian Meyer
# https://plus.google.com/u/0/117404693911977592313?rel=author

# DIY 
class gameConfig(object):
    def __init__(self):
        self.castleCount = 4;
        self.width = 640
        self.height = 480
        self.keys = [False, False, False, False]
        self.playerpos = [100, 100] # init position of player
        self.vol = 0.3
        self.running = 1
        self.exitcode = 0

class protector(object):
    def __init__(self):
        self.acc = [0, 0]
        self.arrows = []
        self.speed = 5
        self.healthvalue = 194

class enemy(object):
    def __init__(self):
        self.damage = 10 
        self.badtime = 100
        self.badtimeAdd = 0
        self.badguys = [[game.width, 100]]
        self.speed = 7

# 2 -Initialize the game
pygame.init()
pygame.mixer.init()
# class above #
game = gameConfig()
rabbit = protector()
badger = enemy()
screen = pygame.display.set_mode((game.width, game.height))

# 3 - Load images
player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
badguyimg1 = pygame.image.load("resources/images/badguy.png")
badguyimg=badguyimg1
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")
# 3.1 - Load audio
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(game.vol)
enemy.set_volume(game.vol)
shoot.set_volume(game.vol)
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(game.vol / 2)

# 4 - keep looping through


while game.running:
    badger.badtime -= 1
    # 5 - clear the screen before drawing it again
    screen.fill(0)
    # 6 - draw the screen elements
    for x in range(game.width / grass.get_width() + 1):
        for y in range(game.height / grass.get_height() + 1):
            screen.blit(grass, (x*grass.get_rect().width, y*grass.get_rect().height))

    ### global x y
    castleHeight = castle.get_rect().height
    pos = (game.height - castleHeight * game.castleCount) / 2
    for i in xrange(game.castleCount):
        screen.blit(castle, (0, pos + castleHeight * i))
    # screen.blit(player, playerpos)
    # 6.1 - Set player position and rotation
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1] - (game.playerpos[1]+32), position[0] - (game.playerpos[0] + 26))
    playerrot = pygame.transform.rotate(player, 360 - angle*57.29)    
    playerposRecorrect = (game.playerpos[0] - playerrot.get_rect().width/2, game.playerpos[1]-playerrot.get_rect().height/2)
    screen.blit(playerrot, playerposRecorrect)
    # 6.2 - Draw rabbit.arrows
    for bullet in rabbit.arrows:
        index = 0
        velx = math.cos(bullet[0]) * 10
        vely = math.sin(bullet[0]) * 10
        bullet[1] += velx
        bullet[2] += vely
        if bullet[1] < -64 or bullet[1] > game.width or bullet[2] < -64 or bullet[2] > game.height:
            rabbit.arrows.pop(index)
        index += 1
        for projectile in rabbit.arrows:
            arrow1 = pygame.transform.rotate(arrow, 360 - projectile[0] * 57.29)
            screen.blit(arrow1, (projectile[1], projectile[2]))
    # 6.3 Draw enemys
    if badger.badtime == 0:
        badger.badguys.append([game.width, random.randint(50, game.height - 50)])
        badger.badtime = 100 - (badger.badtimeAdd * 2)
        if(badger.badtimeAdd >= 35):
            badger.badtimeAdd = 35
        else:
            badger.badtimeAdd += 5
    index = 0
    for badguy in badger.badguys:
        if( badguy[0] < -64):
            badger.badguys.pop(index)
        badguy[0] -= badger.speed
        # 6.3.1 - Attack castle
        badrect = pygame.Rect(badguyimg.get_rect())
        badrect.top = badguy[1]
        badrect.left = badguy[0]
        deadline = castle.get_rect().width / 2  # when cross the line will get damage
        if badrect.left < deadline:
            # section 6.3.1 after if badrect.left<64:
            hit.play()
            rabbit.healthvalue -= random.randint(badger.damage / 2, badger.damage)
            badger.badguys.pop(index)
        # 6.3.2 - Check for collisions
        indexarrow = 0
        for bullet in rabbit.arrows:
            bullrect = pygame.Rect(arrow.get_rect())
            bullrect.left = bullet[1]
            bullrect.top = bullet[2]
            if badrect.colliderect(bullrect):
                # section 6.3.2 after if badrect.colliderect(bullrect):
                enemy.play()
                rabbit.acc[0] += 1
                badger.badguys.pop(index)
                rabbit.arrows.pop(indexarrow)
            indexarrow += 1
        # 6.3.3 - Next bad guy
        index += 1
    for badguy in badger.badguys:
        screen.blit(badguyimg, badguy)
    # 6.4 - Draw clock
    font = pygame.font.Font("resources\YaHei.Consolas.1.11b.ttf", 24)
    survivedtext = font.render(str((90000 - pygame.time.get_ticks()) / 60000) + ":"+str((90000-pygame.time.get_ticks())/1000%60).zfill(2), True, (0,0,0))
    textRect = survivedtext.get_rect()
    textRect.topright = [635, 5]
    screen.blit(survivedtext, textRect)
    # 6.5 - Draw health bar
    screen.blit(healthbar, (5, 5))
    for healthadd in range(rabbit.healthvalue):
        screen.blit(health, (healthadd + 8, 8))
    # 7 - update the screen
    pygame.display.flip()
    # 8 - loop through the events
    for event in pygame.event.get():
        # check if the event is the X button
        if event.type == pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                game.keys[0] = True
            elif event.key==K_a:
                game.keys[1]=True
            elif event.key==K_s:
                game.keys[2]=True
            elif event.key==K_d:
                game.keys[3]=True    
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_w:
                game.keys[0]=False
            elif event.key==pygame.K_a:
                game.keys[1]=False
            elif event.key==pygame.K_s:
                game.keys[2]=False
            elif event.key==pygame.K_d:
                game.keys[3]=False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # section 8, play shooting sound
            shoot.play()
            position = pygame.mouse.get_pos()
            rabbit.acc[1] += 1
            rabbit.arrows.append([math.atan2(position[1] - (playerposRecorrect[1]+32), position[0] - (playerposRecorrect[0]+26)), playerposRecorrect[0]+32, playerposRecorrect[1]+32]) 
    # 9 - Move player
    if game.keys[0]:
        game.playerpos[1] -= rabbit.speed
    elif game.keys[2]:
        game.playerpos[1] += rabbit.speed
    if game.keys[1]:
        game.playerpos[0] -= rabbit.speed
    elif game.keys[3]:
        game.playerpos[0] += rabbit.speed
    # 10 - Win/Lose check
    if pygame.time.get_ticks() >= 90000:
        game.running = 0
        game.exitcode = 1
    if rabbit.healthvalue <= 0:
        game.running = 0
        game.exitcode = 0
    if rabbit.acc[1] != 0:
        rabbit.accuracy = rabbit.acc[0] * 1.0 / rabbit.acc[1] * 100
    else:
        rabbit.accuracy = 0
# 11 - Win/lose display
if game.exitcode == 0:
    pygame.font.init()
    font = pygame.font.Font("resources\YaHei.Consolas.1.11b.ttf", 24)
    text = font.render("Accuracy: " + str(rabbit.accuracy) + "%", True, (255, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
    screen.blit(gameover, (0, 0))
    screen.blit(text, textRect)
else:
    pygame.font.init()
    font = pygame.font.Font("resources\YaHei.Consolas.1.11b.ttf", 24)
    text = font.render("Accuracy:" + str(rabbit.accuracy) + "%", True, (255, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
    screen.blit(youwin, (0, 0))
    screen.blit(text, textRect)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
pygame.quit()
sys.exit()