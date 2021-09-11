#!/usr/bin/env python
# coding: utf-8

# In[1]:


#-*- coding: utf-8 -*-
import pygame
from sys import exit
from pygame.locals import *
import random

# 设置游戏屏幕大小
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 900

# 设置概率函数
def choice(seq, prob):
    p = random.random()
    for i in range(len(seq)):
        if sum(prob[:i]) < p < sum(prob[:i+1]):
            return seq[i]


# In[2]:


# 设置子弹
class Bullet(pygame.sprite.Sprite):
    def __init__(self,init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources/image/love.png').convert()
        self.image.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed


# In[3]:


# 设置炸弹弹片
class Boom(pygame.sprite.Sprite):
    def __init__(self,init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources/image/boom.png').convert()
        self.image.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 15

    def move(self):
        self.rect.top -= self.speed


# In[4]:


# 设置玩家
class Player(pygame.sprite.Sprite):  
    def __init__(self): 
        super().__init__()
        self.image = pygame.image.load('resources/image/Diana.png').convert() # load函数，返回一个 Surface 对象
        self.image.set_colorkey((255,255,255), RLEACCEL)  #白色部分设置为透明
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT * 0.8))
        self.speed = 8    #设置速度
        self.bullets = pygame.sprite.Group()  # 玩家飞机所发射的子弹的集合
        self.is_hit = False  #设置生命
        
    # 发射子弹
    def shoot(self):
        bullet = Bullet(self.rect.midtop)
        self.bullets.add(bullet)
    # 使用炸弹
    def boomuse(self):
        boom = Boom([random.randint(0, SCREEN_WIDTH - 36), SCREEN_HEIGHT + 20])
        self.bullets.add(boom)
        
    # 移动，并判断边界
    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed
    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed
    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed    
    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed


# In[5]:


# 设置敌人
class Enemy(pygame.sprite.Sprite):
    def __init__(self,init_pos):
        super().__init__()
        self.image = pygame.image.load('resources/image/acao.png').convert()
        self.image.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = choice([5,7,9], [0.5, 0.3, 0.2])

    def move(self):
        self.rect.top += self.speed


# In[6]:


# 设置弹药包
class Ammopac(pygame.sprite.Sprite):
    def __init__(self,init_pos):
        super().__init__()
        self.image = pygame.image.load('resources/image/Bella.png').convert()
        self.image.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = 3

    def move(self):
        self.rect.top += self.speed


# In[7]:


# 设置炸弹包
class Boompac(pygame.sprite.Sprite):
    def __init__(self,init_pos):
        super().__init__()
        self.image = pygame.image.load('resources/image/Ava.png').convert()
        self.image.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = 5

    def move(self):
        self.rect.top += self.speed


# In[8]:


# 设置分数包
class Scorepac(pygame.sprite.Sprite):
    def __init__(self,init_pos):
        super().__init__()
        self.image = pygame.image.load('resources/image/Eileen.png').convert()
        self.image.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = 10

    def move(self):
        self.rect.top += self.speed


# In[9]:


# 设置生命包
class Hppac(pygame.sprite.Sprite):
    def __init__(self,init_pos):
        super().__init__()
        self.image = pygame.image.load('resources/image/Carol.png').convert()
        self.image.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = 8

    def move(self):
        self.rect.top += self.speed


# In[10]:


# 准备游戏
# 初始化pygame
pygame.init()
pygame.mixer.init()
# 设置游戏界面大小、背景图片及标题
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('枝江皇牌空战')
background = pygame.image.load('resources/image/background.png').convert()
page1 = pygame.image.load('resources/image/page1.png')
page2 = pygame.image.load('resources/image/page2.png')
page3 = pygame.image.load('resources/image/page3.png')
game_over = pygame.image.load('resources/image/gameover.png')
font = pygame.font.Font('resources/font/font.ttf', 40)
#font = pygame.font.SysFont('arial', 16)
#创建玩家
player = Player()
# 存储敌机和被击毁敌机
enemies = pygame.sprite.Group()
enemies_down = pygame.sprite.Group()
# 存储补给包
ammopacs = pygame.sprite.Group()
boompacs = pygame.sprite.Group()
scorepacs = pygame.sprite.Group()
hppacs = pygame.sprite.Group()
# 播放BGM
pygame.mixer.music.load(r'resources/se/bgm.ogg')
pygame.mixer.music.set_volume(1.2)
pygame.mixer.music.play()
# 加载音效
boomsound = pygame.mixer.Sound(r'resources/se/boom.ogg')
boomsound.set_volume(1)
gameoversound = pygame.mixer.Sound(r'resources/se/gameover.ogg')
gameoversound.set_volume(1)
bellasound1 = pygame.mixer.Sound(r'resources/se/bella1.ogg')
bellasound1.set_volume(0.8)
bellasound2 = pygame.mixer.Sound(r'resources/se/bella2.ogg')
bellasound2.set_volume(1)
bellasound3 = pygame.mixer.Sound(r'resources/se/bella3.ogg')
bellasound3.set_volume(1)
avasound = pygame.mixer.Sound(r'resources/se/ava.ogg')
avasound.set_volume(0.8)
elieensound = pygame.mixer.Sound(r'resources/se/elieen.ogg')
elieensound.set_volume(1)
carolsound = pygame.mixer.Sound(r'resources/se/carol.ogg')
carolsound.set_volume(1)
shootsound = pygame.mixer.Sound(r'resources/se/shoot.ogg')
shootsound.set_volume(0.13)
downsound = pygame.mixer.Sound(r'resources/se/down.ogg')
downsound.set_volume(0.13)
# 初始化参数
shoot_frequency = 0
boom_frequency = 0
enemy_frequency = 0
ammopac_frequency = 0
boompac_frequency = 0
scorepac_frequency = 0
hppac_frequency = 0
life = 1
ammo = 30
boom = 1
boomnum = 0
score = 0
# 游戏循环帧率设置
clock = pygame.time.Clock()
# 判断游戏循环退出的参数
running = True
start1 = False
start2 = False
start3 = False
gap = 0
playgos = True


# In[11]:


# 游戏主循环
while running == True:
    # 控制游戏最大帧率为 60
    clock.tick(60)
    # 填充背景
    screen.fill(0)
    screen.blit(background, (0, 0))
    # 获取键盘事件（按键）
    key_pressed = pygame.key.get_pressed()
    
    # 开始前界面
    while start1 == False:
        clock.tick(60)
        key_pressed = pygame.key.get_pressed()
        screen.blit(page1,(0,0))
        pygame.display.flip()
        if key_pressed[K_SPACE]:
            start1 = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    while start2 == False:
        clock.tick(60)
        key_pressed = pygame.key.get_pressed()
        screen.blit(page2,(0,0))
        pygame.display.flip()
        gap += 1
        if key_pressed[K_SPACE] and gap > 40:
            start2 = True
            gap = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    while start3 == False:
        clock.tick(60)
        key_pressed = pygame.key.get_pressed()
        screen.blit(page3,(0,0))
        pygame.display.flip()
        gap += 1
        if key_pressed[K_1] and gap > 30:
            level = 1
            start3 = True
            gap = 0
        if key_pressed[K_2] and gap > 30:
            level = 2
            start3 = True
            gap = 0
        if key_pressed[K_3] and gap > 30:
            level = 3
            start3 = True
            gap = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
    # Game Over后显示最终得分
    while player.is_hit == True:
        clock.tick(60)
        key_pressed = pygame.key.get_pressed()
        if playgos == True:
            gameoversound.play()
            playgos = False
        # 游戏结束图片
        screen.blit(game_over, (0,0))
        # 显示得分
        text = font.render('Final Score: '+ str(score), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.centery = screen.get_rect().centery + 24
        screen.blit(text, text_rect)
        pygame.display.flip()
        if key_pressed[K_r]:
            # 重置游戏状态
            enemies = pygame.sprite.Group()
            player.bullets = pygame.sprite.Group()
            enemies_down = pygame.sprite.Group()
            ammopacs = pygame.sprite.Group()
            boompacs = pygame.sprite.Group()
            scorepacs = pygame.sprite.Group()
            hppacs = pygame.sprite.Group()
            shoot_frequency = 0
            boom_frequency = 0
            enemy_frequency = 0
            ammopac_frequency = 0
            boompac_frequency = 0
            scorepac_frequency = 0
            hppac_frequency = 0
            player.rect = player.image.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT * 0.8))
            life = 1
            ammo = 30
            boom = 1
            boomnum = 0
            score = 0
            player.is_hit = False
            playgos = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    
    ########### 键 盘 处 理 ###########
    # 处理键盘事件（移动飞机的位置）
    if key_pressed[K_w] or key_pressed[K_UP]:
        player.moveUp()
    if key_pressed[K_s] or key_pressed[K_DOWN]:
        player.moveDown()
    if key_pressed[K_a] or key_pressed[K_LEFT]:
        player.moveLeft()
    if key_pressed[K_d] or key_pressed[K_RIGHT]:
        player.moveRight()
    # 处理键盘事件（玩家开火）
    if not player.is_hit:
        if key_pressed[K_SPACE]:
            if ammo > 0:
                if shoot_frequency > 15:
                    player.shoot()
                    ammo -= 1
                    shootsound.play()
                    shoot_frequency = 0
        shoot_frequency += 1
        if shoot_frequency > 200:
            shoot_frequency = 16
    # 处理键盘事件（使用炸弹）
    if not player.is_hit:
        if key_pressed[K_f]:
            if boom > 0:
                if boom_frequency >30:
                    boomnum += 40
                    boom -= 1
                    boom_frequency = 0
                    boomsound.play()
        boom_frequency += 1
        if boom_frequency > 200:
            boom_frequency = 31
        if boomnum > 0:
            player.boomuse()
            boomnum -= 1

    # 以固定速度移动子弹
    for bullet in player.bullets:
        bullet.move()
        # 移动出屏幕后删除子弹
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)   

########### 敌 机 处 理 ###########

    # 生成敌机，并控制生成频率
    # 循环18次生成一架敌机
    if enemy_frequency > 17: 
        enemy_pos = [random.randint(0, SCREEN_WIDTH - 52), 0]
        enemy1 = Enemy(enemy_pos)
        enemies.add(enemy1)
        enemy_frequency = 0  
    if level == 1:
        enemy_frequency += 0.6
    if level == 2:
        enemy_frequency += 1 
    if level == 3:
        enemy_frequency += 1.2
    # 移动敌机
    for enemy in enemies:
        enemy.move()
        # 敌机与玩家飞机碰撞效果处理
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies.remove(enemy)
            downsound.play()
            life -= 1
            if life < 1:
               player.is_hit = True
            
        # 移动出屏幕后删除敌人
        if enemy.rect.top < 0:
            enemies.remove(enemy)
    
    # 敌机被子弹击中效果处理
    # 将被击中的敌机对象添加到击毁敌机 Group 中
    enemies1_down = pygame.sprite.groupcollide(enemies, player.bullets, 1, 1)
    for enemy_down in enemies1_down:
        enemies_down.add(enemy_down)
    # 敌机被子弹击中效果显示
    for enemy_down in enemies_down:
        enemies_down.remove(enemy_down)
        downsound.play()
        score += 1
    
########### 弹 药 处 理 ###########
        
    # 循环200次生成一个弹药包
    if ammopac_frequency > 199:
        ammopac_pos = [random.randint(0, SCREEN_WIDTH - 52), 0]
        ammopac = Ammopac(ammopac_pos)
        ammopacs.add(ammopac)
        ammopac_frequency = 0  
    ammopac_frequency += 1 
    # 弹药包移动
    for ammopac in ammopacs:
        ammopac.move()
        # 玩家拾取弹药包
        if pygame.sprite.collide_circle(ammopac, player):
            ammopacs.remove(ammopac)
            ammo += 10
            bellarand = choice([1,2,3], [0.4, 0.3, 0.3])
            if bellarand ==1:
                bellasound1.play()
            elif bellarand ==2:
                bellasound2.play()
            elif bellarand ==3:
                bellasound3.play()
        # 移动出屏幕后删除弹药包
        if ammopac.rect.top < 0:
            ammopacs.remove(ammopac)

########### 分 数 包 处 理 ###########
        
    # 循环400次生成一个分数包
    if scorepac_frequency > 399:
        scorepac_pos = [random.randint(0, SCREEN_WIDTH - 52), 0]
        scorepac = Scorepac(scorepac_pos)
        scorepacs.add(scorepac)
        scorepac_frequency = 0  
    scorepac_frequency += 1 
    # 分数包移动
    for scorepac in scorepacs:
        scorepac.move()
        # 玩家拾取分数包
        if pygame.sprite.collide_circle(scorepac, player):
            scorepacs.remove(scorepac)
            score += 10
            elieensound.play()
        # 移动出屏幕后删除分数包
        if scorepac.rect.top < 0:
            scorepacs.remove(scorepac)

########### 炸 弹 包 处 理 ###########
        
    # 循环800次生成一个炸弹包
    if boompac_frequency > 799:
        boompac_pos = [random.randint(0, SCREEN_WIDTH - 52), 0]
        boompac = Boompac(boompac_pos)
        boompacs.add(boompac)
        boompac_frequency = 0  
    boompac_frequency += 1 
    # 炸弹包移动
    for boompac in boompacs:
        boompac.move()
        # 玩家拾取弹药包
        if pygame.sprite.collide_circle(boompac, player):
            boompacs.remove(boompac)
            boom += 1
            avasound.play()
            
        # 移动出屏幕后删除弹药包
        if boompac.rect.top < 0:
            boompacs.remove(boompac)

########### 生 命 包 处 理 ###########
        
    # 循环1600次生成一个生命包
    if hppac_frequency > 1599:
        hppac_pos = [random.randint(0, SCREEN_WIDTH - 52), 0]
        hppac = Hppac(hppac_pos)
        hppacs.add(hppac)
        hppac_frequency = 0  
    hppac_frequency += 1 
    # 生命包移动
    for hppac in hppacs:
        hppac.move()
        # 玩家拾取生命包
        if pygame.sprite.collide_circle(hppac, player):
            hppacs.remove(hppac)
            life += 1
            carolsound.play()
        # 移动出屏幕后删除弹药包
        if hppac.rect.top < 0:
            hppacs.remove(hppac)
            
########### 绘 制 图 像 ###########
    
    # 绘制玩家飞机
    if not player.is_hit:
        screen.blit(player.image, player.rect) #将正常飞机画出来

    # 绘制得分
    score_text = font.render('得分: '+str(score), True, (128, 128, 128))
    score_rect = score_text.get_rect()
    score_rect.topleft = [10, 30]
    screen.blit(score_text, score_rect)
    
    # 绘制生命值
    life_text = font.render('生命: '+str(life), True, (128, 128, 128))
    life_rect = life_text.get_rect()
    life_rect.topleft = [10, 70]
    screen.blit(life_text, life_rect)
    
    # 绘制子弹数量
    ammo_text = font.render('子弹: '+str(ammo), True, (128, 128, 128))
    ammo_rect = ammo_text.get_rect()
    ammo_rect.topleft = [10, 110]
    screen.blit(ammo_text, ammo_rect)

    # 绘制炸弹数量
    boom_text = font.render('一个魂: '+str(boom), True, (128, 128, 128))
    boom_rect = boom_text.get_rect()
    boom_rect.topleft = [10, 150]
    screen.blit(boom_text, boom_rect)

    # 绘制各单位
    player.bullets.draw(screen)
    enemies.draw(screen)
    ammopacs.draw(screen)
    boompacs.draw(screen)
    scorepacs.draw(screen)
    hppacs.draw(screen)
    
    # 更新屏幕
    pygame.display.flip()
    # 处理游戏退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

