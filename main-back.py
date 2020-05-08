# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import math
import sys
import random
from imglibrary import *
from SElibrary import *

#$-Find Index-$---
# EnemyClass
#-----------------

#普通の弾　ギミック:なし
class MainGame:
    def __init__(self):
        pygame.mixer.quit()
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()

        global screen
        screen = pygame.display.set_mode([640,480],FULLSCREEN)
        pygame.display.set_caption("Test")
        count = 0
        self.ready = 0
        self.backgroundpattern = 0
        self.by = [-64]
        self.zanki = 3
        self.wireframe = (0, 255, 0)
        for i in range(0, 10, 1):
            self.by.append(i * 64)
        self.px = 180
        self.py = 370
        self.backspeed = 0
        self.Boss = 0
        self.Timer = 0
        self.scroll = 0
        self.BossFlag = 0

        self.ex = 320
        self.ey = 60
        self.debug = 1
        self.score = 0
        global ShotDamage
        ShotDamage = 10
        self.initgame()
        clock = pygame.time.Clock()
        self.sysfont = pygame.font.SysFont(None,40)

        while 1:
            pygame.display.update()
            clock.tick(60)
            self.update()
            self.draw(screen)

    def initgame(self):
        # 初期化　グローバル変数宣言　など
        global Bomb
        global OneUp
        global ScoreI100
        global ScoreI300
        global ScoreI500
        global ScoreI900
        global ScoreI2000
        global ScoreI5000
        global ScoreI10000

        Bomb = ItemBomb
        OneUp = Item1UP
        ScoreI100 = ItemScore100
        ScoreI300 = ItemScore300
        ScoreI500 = ItemScore500
        ScoreI900 = ItemScore900
        ScoreI2000 = ItemScore2000
        ScoreI5000 = ItemScore5000
        ScoreI10000 = ItemScore10000

        global NormalShot
        global CurveShot
        global CurveShot2
        global TurboShot
        global TurboShot2
        global TurboShot3
        global TurboShot4
        global BoundShot
        global VanishShot
        global BulletHorming
        global GravityShot
        global PlayerShot

        NormalShot = BulletNormal
        CurveShot = BulletCurve
        CurveShot2 = BulletCurve2
        TurboShot = BulletTurbo
        TurboShot2 = BulletTurbo2
        TurboShot3 = BulletTurbo3
        TurboShot4 = BulletTurbo4
        BoundShot = BulletBound
        VanishShot = BulletVanish
        #HormingShot = BulletHorming
        GravityShot = BulletGravity
        PlayerShot = BulletPlayer

        global ScoreE100
        global ScoreE300
        global ScoreE500
        global ScoreE5000
        global ScoreE10000

        ScoreE100 = ScoreEnemy100
        ScoreE300 = ScoreEnemy300
        ScoreE500 = ScoreEnemy500
        ScoreE5000 = ScoreEnemy5000
        ScoreE10000 = ScoreEnemy10000

        global jiki
        jiki = PlayerJIKI
        global EnemyTest
        EnemyTest = TestEnemy

        self.all = pygame.sprite.RenderUpdates()
        self.bulletgroup = pygame.sprite.Group()
        self.Playergroup = pygame.sprite.Group()
        self.jikigroup = pygame.sprite.Group()
        self.Itemgroup = pygame.sprite.Group()
        self.Enemygroup = pygame.sprite.Group()
        self.Scoregroup1 = pygame.sprite.Group()
        self.Scoregroup2 = pygame.sprite.Group()
        self.Scoregroup3 = pygame.sprite.Group()
        self.Scoregroup4 = pygame.sprite.Group()
        self.Scoregroup5 = pygame.sprite.Group()
        self.Scoregroup6 = pygame.sprite.Group()
        self.Scoregroup7 = pygame.sprite.Group()

        NormalShot.containers = self.bulletgroup,self.all
        CurveShot.containers = self.bulletgroup, self.all
        CurveShot2.containers = self.bulletgroup, self.all
        TurboShot.containers = self.bulletgroup, self.all
        TurboShot2.containers = self.bulletgroup, self.all
        TurboShot3.containers = self.bulletgroup, self.all
        TurboShot4.containers = self.bulletgroup, self.all
        BoundShot.containers = self.bulletgroup, self.all
        VanishShot.containers = self.bulletgroup, self.all
        GravityShot.containers = self.bulletgroup,self.all

        jiki.containers = self.all,self.jikigroup
        PlayerShot.containers = self.all,self.Playergroup
        EnemyTest.containers = self.all,self.Enemygroup
        Enemy1.containers = self.all,self.Enemygroup
        Enemy2.containers = self.all,self.Enemygroup
        Stage1MBoss.containers = self.all,self.Enemygroup
        Stage1boss.containers = self.all,self.Enemygroup

        Bomb.containers = self.all
        OneUp.containers = self.all
        ScoreI100.containers = self.all,self.Scoregroup1
        ScoreI300.containers = self.all,self.Scoregroup2
        ScoreI500.containers = self.all,self.Scoregroup3
        ScoreI900.containers = self.all,self.Scoregroup4
        ScoreI2000.containers = self.all,self.Scoregroup5
        ScoreI5000.containers = self.all,self.Scoregroup6
        ScoreI10000.containers = self.all,self.Scoregroup7
        ScoreE100.containers = self.all,self.Enemygroup
        ScoreE300.containers = self.all,self.Enemygroup
        ScoreE500.containers = self.all,self.Enemygroup
        ScoreE5000.containers = self.all,self.Enemygroup
        ScoreE10000.containers = self.all,self.Enemygroup

        self.Pla = jiki(PLAYER,self.px,self.py)

        NormalShot.Pla = self.Pla
        CurveShot.Pla = self.Pla
        CurveShot2.Pla = self.Pla
        TurboShot.Pla = self.Pla
        TurboShot2.Pla = self.Pla
        TurboShot3.Pla = self.Pla
        TurboShot4.Pla = self.Pla
        BoundShot.Pla = self.Pla
        VanishShot.Pla = self.Pla
        GravityShot.Pla = self.Pla
        EnemyTest.Pla = self.Pla
        Enemy1.Pla = self.Pla
        Enemy2.Pla = self.Pla
        Stage1MBoss.Pla = self.Pla
        Stage1boss.Pla = self.Pla
        ScoreE100.Pla = self.Pla
        ScoreE300.Pla = self.Pla
        ScoreE500.Pla = self.Pla
        ScoreE5000.Pla = self.Pla
        ScoreE10000.Pla = self.Pla
        PlayerShot.score = self.score

        #------------------------------
        EnemyTest.Hit = Enemy1.Hit = Enemy2.Hit =self.Playergroup
        ScoreE100.Hit = ScoreE300.Hit = ScoreE500.Hit = ScoreE5000.Hit = ScoreE10000.Hit = self.Playergroup
        Stage1MBoss.Hit = Stage1boss.Hit = self.Playergroup
        #------------------------------
        PlayerShot.EHit = self.Enemygroup
        PlayerJIKI.EHit = self.bulletgroup
        global PBomb_sound
        global shoot_sound
        global Player_Hit_sound
        PBomb_sound = pygame.mixer.Sound(PBomb)
        shoot_sound = pygame.mixer.Sound(shoot)
        Player_Hit_sound = pygame.mixer.Sound(Player_Hit)
        #------------------------------

    def update(self):
        self.scroll += 1
        # 更新　エスケープキーを押すと終了処理をする
        if self.zanki == 1:
            ZankiFColor = (255,0,0)
        else :
            ZankiFColor = (255,255,255)
        self.scoreF = self.sysfont.render("Score:{}".format(self.score),True,ZankiFColor)
        self.BombF = self.sysfont.render("Bomb:{}".format(self.Pla.hasbomb),True,ZankiFColor)
        self.ZankiF = self.sysfont.render("zanki:{}".format(self.zanki),True,ZankiFColor)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        self.all.update()

        #デバッグ用
        self.Timer += 1
        count = 0

        if self.debug == 1:
            #デバッグステージ

            if self.scroll == 240:
                Enemy2(180,-50,100,1,4)
            if self.scroll == 600:
                Enemy1(240,-80,100,1,5)
            if self.scroll == 1800:
                self.Boss = Stage1MBoss(250,-80)
                self.BossFlag = 1
                self.scroll += 1
            if self.scroll == 2000:
                Enemy2(90,-50,100,2,4)
                Enemy2(120, -50, 100, 1, 4)
                Enemy2(200, -50, 100, 1, 4)
                Enemy2(240, -50, 100, 2, 4)
            if self.scroll == 2100:
                Enemy1(90,-50,100,2,4)
                Enemy1(120, -50, 100, 1, 4)
                Enemy1(200, -50, 100, 1, 4)
                Enemy1(240, -50, 100, 2, 4)
            if self.scroll == 2300:
                Enemy2(90,-50,100,1,4)
                Enemy1(120, -50, 100, 3, 4)
                Enemy1(200, -50, 100, 3, 4)
                Enemy2(240, -50, 100, 1, 4)
            if self.scroll == 240:
                self.Boss = Stage1boss(250,-80)
                self.BossFlag = 1
                self.scroll += 1

            #演出用
            if self.scroll == 240:
                self.backspeed = 1
            if self.BossFlag == 1 and (self.scroll <= 1803 and self.scroll >= 1800):
                self.backspeed = 0
            if self.scroll == 2000:
                self.backspeed = 1
            if self.scroll == 2400:
                self.backspeed = 3
            if self.scroll == 2600:
                self.backspeed = 5
            if self.scroll == 285:
                self.backspeed = 9
            if self.BossFlag == 1 and (self.scroll <= 3263 and self.scroll >= 3260):
                self.backspeed = 9

        if self.BossFlag == 1:
            self.scroll -= 1
            if self.Boss.HP >= 1:
                self.BossHP = self.sysfont.render("Target:{}%".format(math.floor((self.Boss.HP/self.Boss.HPMAX)*100)), True, ZankiFColor)
            elif self.Boss.HP <= 0:
                self.BossFlag = 0

        #当たり判定集　やむを得ない処置
        #Playercollide = pygame.sprite.spritecollide(self.Pla,self.bulletgroup,False,pygame.sprite.collide_circle)
        Enemycollide = pygame.sprite.groupcollide(self.Playergroup,self.Enemygroup,False,False,pygame.sprite.collide_circle)
        Score100collide = pygame.sprite.spritecollide(self.Pla,self.Scoregroup1,True,pygame.sprite.collide_circle)
        Score300collide = pygame.sprite.spritecollide(self.Pla,self.Scoregroup2,True,pygame.sprite.collide_circle)
        Score500collide = pygame.sprite.spritecollide(self.Pla,self.Scoregroup3,True,pygame.sprite.collide_circle)
        Score900collide = pygame.sprite.spritecollide(self.Pla,self.Scoregroup4,True,pygame.sprite.collide_circle)
        Score2000collide = pygame.sprite.spritecollide(self.Pla,self.Scoregroup5,True,pygame.sprite.collide_circle)
        Score5000collide = pygame.sprite.spritecollide(self.Pla,self.Scoregroup6,True,pygame.sprite.collide_circle)
        Score10000collide = pygame.sprite.spritecollide(self.Pla,self.Scoregroup7,True,pygame.sprite.collide_circle)

        if self.zanki == 0:
            print("あなたの得点は{}点です".format(self.score))
            pygame.quit()
            sys.exit()

        if self.Pla.deathflag == 1 and self.zanki > 0:
            self.zanki -= 1
            self.Pla = jiki(PLAYER,self.px,self.py)
            NormalShot.Pla = self.Pla
            CurveShot.Pla = self.Pla
            CurveShot2.Pla = self.Pla
            TurboShot.Pla = self.Pla
            TurboShot2.Pla = self.Pla
            TurboShot3.Pla = self.Pla
            TurboShot4.Pla = self.Pla
            BoundShot.Pla = self.Pla
            VanishShot.Pla = self.Pla
            EnemyTest.Pla = self.Pla
            Enemy1.Pla = self.Pla
            Enemy2.Pla = self.Pla
            Stage1MBoss.Pla = self.Pla
            Stage1boss.Pla = self.Pla
            ScoreE100.Pla = self.Pla
            ScoreE300.Pla = self.Pla
            ScoreE500.Pla = self.Pla
            ScoreE5000.Pla = self.Pla
            ScoreE10000.Pla = self.Pla
            self.PlayerDead = 0
        if Enemycollide:
            self.score += 10

        #if PlayerShot.Plus == 1:
        #    self.score += 20

        if Score100collide:
            self.score += 100
        if Score300collide:
            self.score += 300
        if Score500collide:
            self.score += 500
        if Score900collide:
            self.score += 900
        if Score2000collide:
            self.score += 2000
        if Score5000collide:
            self.score += 5000
        if Score10000collide:
            self.score += 10000

        pygame.display.flip()
        pygame.display.update()

    def draw(self,screen):
        #描画 ワイヤーフレーム背景
        screen.fill((0, 0, 0))
        if self.backgroundpattern == 0:
            for j in range(0, 11, 1):
                pygame.draw.line(screen, self.wireframe, (0, self.by[j]), (640, self.by[j]), 1)
                self.by[j] += self.backspeed
                if self.by[j] > 640:
                    self.by[j] = -64
                if self.by[j] < -65:
                    self.by[j] = 640
            for i in range(0,11,1):
                pygame.draw.line(screen, self.wireframe, (i*63, 0), (i*63, 480), 1)
        self.all.draw(screen)
        screen.blit(self.scoreF,(0,0))
        screen.blit(self.BombF,(0,25))
        screen.blit(self.ZankiF,(0,50))
        if self.BossFlag == 1:
            if self.Boss.HP >= 1:
                screen.blit(self.BossHP,(475,0))

class ItemBomb(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(BombG).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = 0
        self.vy = 1.25
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y

        RectKill(self)

    def draw(self,screen):
        screen.blit(self.image.self.rect)

class Item1UP(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(OneUPG).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = 0
        self.vy = 1.25
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y

        RectKill(self)

    def draw(self,screen):
        screen.blit(self.image.self.rect)
'''
class ItemScore(pygame.sprite.Sprite):
    def __init__(self,x,y,value=0):
        pygame.sprite.Sprite.__init__(self,self.containers)
        if value >= 7 :
            value = 6
        elif value <= -1 :
            value = 0
        self.value = value
        self.ScoreG = [Score100,Score300,Score500,Score900,Score2000,Score5000,Score10000]
        self.image = pygame.image.load(self.ScoreG[self.value]).convert_alpha()
        self.ScoreList = [100,300,500,900,2000,5000,10000]
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = 0
        self.vy = 1.25
        self.score = self.ScoreList[self.value]


    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y
        self.score = self.ScoreList[self.value]

        if self.score == 0:
            self.kill()

        RectKill(self)

    def draw(self,screen):
        screen.blit(self.image.self.rect)
'''

class ItemScore100(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.ScoreG = [Score100,Score300,Score500,Score900,Score2000,Score5000,Score10000]
        self.image = pygame.image.load(Score100).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = 0
        self.vy = 1.25
        self.score = 100

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y

        RectKill(self)

    def draw(self,screen):
        screen.blit(self.image.self.rect)

class ItemScore300(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.ScoreG = [Score100,Score300,Score500,Score900,Score2000,Score5000,Score10000]
        self.image = pygame.image.load(Score300).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = 0
        self.vy = 1.25
        self.score = 300


    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y

        RectKill(self)

    def draw(self,screen):
        screen.blit(self.image.self.rect)

class ItemScore500(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.ScoreG = [Score100,Score300,Score500,Score900,Score2000,Score5000,Score10000]
        self.image = pygame.image.load(Score500).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = 0
        self.vy = 1.25
        self.score = 500


    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y

        RectKill(self)

    def draw(self,screen):
        screen.blit(self.image.self.rect)

class ItemScore900(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.ScoreG = [Score100,Score300,Score500,Score900,Score2000,Score5000,Score10000]
        self.image = pygame.image.load(Score900).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = 0
        self.vy = 1.25
        self.score = 900


    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y

        RectKill(self)

    def draw(self,screen):
        screen.blit(self.image.self.rect)

class ItemScore2000(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.ScoreG = [Score100,Score300,Score500,Score900,Score2000,Score5000,Score10000]
        self.image = pygame.image.load(Score2000).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = 0
        self.vy = 1.25
        self.score = 2000


    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y

        RectKill(self)

    def draw(self,screen):
        screen.blit(self.image.self.rect)

class ItemScore5000(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.ScoreG = [Score100,Score300,Score500,Score900,Score2000,Score5000,Score10000]
        self.image = pygame.image.load(Score5000).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = 0
        self.vy = 1.25
        self.score = 5000


    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y

        RectKill(self)

    def draw(self,screen):
        screen.blit(self.image.self.rect)

class ItemScore10000(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.ScoreG = [Score100,Score300,Score500,Score900,Score2000,Score5000,Score10000]
        self.image = pygame.image.load(Score10000).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = 0
        self.vy = 1.25
        self.score = 10000

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y

        RectKill(self)

    def draw(self,screen):
        screen.blit(self.image.self.rect)

class BulletNormal(pygame.sprite.Sprite):
    def __init__(self,filename,x,y,speed,angle,NotRadian=0,BombResist=0):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        x -= width/2
        y -= height/2
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.center = (x/width,y/height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.angle = math.radians(angle) * 180 /math.pi
        if NotRadian == 0:
            self.angle = math.radians(angle)
        elif NotRadian == 1:
            self.angle = angle
        if self.angle >= 360:
            self.angle -= 360
        self.speed = speed
        self.vx = math.cos(self.angle) *self.speed
        self.vy = math.sin(self.angle) *self.speed
        self.radius = (width/6) + (height/6)
        self.timer = 120
        self.BombResist = BombResist

    def update(self):
        #self.rect.move_ip(self.rect.x,self.rect.y)
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y

        self.timer -=1
        if (self.Pla.bombflag or self.Pla.BulletAnti) and self.BombResist == 0:
            self.kill()

        RectKill(self)

    def draw(self,screen):
        screen.blit(self.image.self.rect)

#カーブ弾　ギミック:有効時間内に角度が徐々に曲がる
class BulletCurve(pygame.sprite.Sprite):
    def __init__(self,filename,x,y,speed,angle,Vangle,timer,NotRadian=0,BombResist=0):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        x -= width/2
        y -= height/2
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.angle = angle
        if NotRadian == 0:
            self.angle = math.radians(angle)
            self.Vangle = math.radians(Vangle)
        elif NotRadian == 1:
            self.angle = angle
            self.Vangle = Vangle
        self.Vangle = math.radians(Vangle)
        if self.angle >= 360:
            self.angle -= 360
        self.speed = speed
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        self.timer = timer
        self.radius = (width/6) + (height/6)
        self.BombResist = BombResist
    def update(self):
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y
        if(self.Pla.bombflag or self.Pla.BulletAnti) and self.BombResist == 0:
            self.kill()
        self.timer -= 1

        if self.timer >= 0:
            self.angle += self.Vangle
        if self.timer <= 0:
            self.timer = 0

        RectKill(self)

    def draw(self,screen):
        screen.blit(self.image.self.rect)

#カーブ弾2　ギミック:指定された時間に経つと、角度を変更する　また回数を指定するとその回数分繰り返す
class BulletCurve2(pygame.sprite.Sprite):
    def __init__(self,filename,x,y,speed,angle,time,Vangle,count=1,NotRadian=0,BombResist=0):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        x -= width/2
        y -= height/2
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        if NotRadian == 0:
            self.angle = math.radians(angle)
            self.Vangle = math.radians(Vangle)
        elif NotRadian == 1:
            self.angle = angle
            self.Vangle = Vangle
        self.speed = speed
        self.Resettime = time
        self.Time = time
        self.count = count
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        self.radius = (width/6) + (height/6)
        self.BombResist = BombResist
    def update(self):
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y
        if self.angle >= 360:
            self.angle -= 360

        RectKill(self)
        if self.count>0:
            self.Time -=1
            if self.Time <=0:
                self.angle += self.Vangle
                self.Time = self.Resettime
                self.count -= 1

        if (self.Pla.bombflag or self.Pla.BulletAnti) and self.BombResist == 0:
            self.kill()

    def draw(self,screen):
        screen.blit(self.image.self.rect)

#加速弾    ギミック:徐々に加速する
class BulletTurbo(pygame.sprite.Sprite):
    def __init__(self,filename,x,y,speed,angle,vspeed,NotRadian=0,BombResist=0):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        x -= width/2
        y -= height/2
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        if NotRadian == 0:
            self.angle = math.radians(angle)
        elif NotRadian == 1:
            self.angle = angle
        if self.angle >= 360:
            self.angle -= 360
        self.speed = speed
        self.vspeed = vspeed
        self.vx = math.cos(self.angle) *self.speed
        self.vy = math.sin(self.angle) *self.speed
        self.radius = (width/6) + (height/6)
        self.BombResist = BombResist
    def update(self):
        #self.rect.move_ip(self.rect.x,self.rect.y)
        self.vx = math.cos(self.angle) *self.speed
        self.vy = math.sin(self.angle) *self.speed
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed += self.vspeed/10

        if (self.Pla.bombflag or self.Pla.BulletAnti) and self.BombResist == 0:
            self.kill()

        RectKill(self)

    def draw(self,screen):
        screen.blit(self.image.self.rect)

#加速弾2       ギミック:時間指定で加速する
class BulletTurbo2(pygame.sprite.Sprite):
    def __init__(self,filename,x,y,speed,angle,time,vspeed,NotRadian=0,BombResist=0):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        x -= width/2
        y -= height/2
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        if NotRadian == 0:
            self.angle = math.radians(angle)
        elif NotRadian == 1:
            self.angle = angle
        if self.angle >= 360:
            self.angle -= 360
        self.speed = speed
        self.vspeed = vspeed
        self.time = time
        self.vx = math.cos(self.angle) *self.speed
        self.vy = math.sin(self.angle) *self.speed
        self.radius = (width/6) + (height/6)
        self.BombResist = BombResist
    def update(self):
        #self.rect.move_ip(self.rect.x,self.rect.y)
        self.vx = math.cos(self.angle) *self.speed
        self.vy = math.sin(self.angle) *self.speed
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y

        self.time -= 1

        if self.time <= 0:
            self.speed += self.vspeed

        if (self.Pla.bombflag or self.Pla.BulletAnti) and self.BombResist == 0:
            self.kill()

        RectKill(self)

    def draw(self,screen):
        screen.blit(self.image.self.rect)

#加速弾3   ギミック:指定時間で、一旦停止し、指定したスピードで再び動く  オプション:角度変化,角度変化の仕方(0なら加算,1なら代入),加速の仕方(0なら徐々に,1なら急加速)
class BulletTurbo3(pygame.sprite.Sprite):
    def __init__(self,filename,x,y,speed,angle,stoptime,vspeed,starttime,vangle=0,hangle=0,speedb=0,NotRadian=0,BombResist=0):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        x -= width/2
        y -= height/2
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        if NotRadian == 0:
            self.angle = math.radians(angle)
            self.vangle = math.radians(vangle)
        elif NotRadian == 1:
            self.angle = angle
            self.vangle = vangle
        if self.angle >= 360:
            self.angle -= 360
        self.speed = speed
        self.stoptime = stoptime
        self.starttime = starttime
        self.vspeed = vspeed
        self.hangle = hangle & 1
        self.eangle = 0
        self.speedb = speedb & 1
        self.vx = math.cos(self.angle) *self.speed
        self.vy = math.sin(self.angle) *self.speed
        self.radius = (width/6) + (height/6)
        self.BombResist = BombResist
    def update(self):
        #self.rect.move_ip(self.rect.x,self.rect.y)
        self.vx = math.cos(self.angle) *self.speed
        self.vy = math.sin(self.angle) *self.speed
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y

        self.stoptime -= 1
        if self.stoptime <= 0:
            self.stoptime = 0
            self.speed -= self.speed/10
            if self.speed < 0:
                self.speed = 0
            self.starttime -= 1
            if self.starttime <= 0:
                if self.vangle >= 1:
                    if self.hangle == 0 and  self.eangle == 0:
                        self.angle += self.vangle
                        self.eangle = 1
                    elif self.hangle == 1 and self.eangle == 0:
                        self.angle = self.vangle
                        self.eangle = 1
                if self.speedb == 0:
                    self.speed += self.vspeed/10
                    if self.speed >= self.vspeed:
                        self.speed = self.vspeed
                elif self.speedb == 1:
                    self.speed = self.vspeed

        if (self.Pla.bombflag or self.Pla.BulletAnti) and self.BombResist == 0:
            self.kill()

        RectKill(self)

    def draw(self,screen):
        screen.blit(self.image.self.rect)

#加速弾4   ギミック:時間指定で徐々に減速し、急加速する
class BulletTurbo4(pygame.sprite.Sprite):
    def __init__(self,filename,x,y,speed,angle,vspeed,time,NotRadian=0,BombResist=0):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        x -= width/2
        y -= height/2
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        if NotRadian == 0:
            self.angle = math.radians(angle)
        elif NotRadian == 1:
            self.angle = angle
        if self.angle >= 360:
            self.angle -= 360
        self.speed = speed
        self.vspeed = vspeed
        self.time = time
        self.timelimit = time
        self.stop = 0
        self.vx = math.cos(self.angle) *self.speed
        self.vy = math.sin(self.angle) *self.speed
        self.radius = (width/6) + (height/6)
        self.BombResist = BombResist
    def update(self):
        #self.rect.move_ip(self.rect.x,self.rect.y)
        self.vx = math.cos(self.angle) *self.speed
        self.vy = math.sin(self.angle) *self.speed
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y

        if self.stop == 0:
            self.time -= 1
        if self.time <= 0:
            self.stop = 1
            self.speed = self.speed/10
        if self.stop == 1:
            self.time += 1
        if self.time >= self.timelimit:
            self.speed = self.vspeed

        if (self.Pla.bombflag or self.Pla.BulletAnti) and self.BombResist == 0:
            self.kill()

        RectKill(self)

    def draw(self,screen):
        screen.blit(self.image.self.rect)

#バウンド弾      ギミック:壁に衝突すると、跳ね返る
class BulletBound(pygame.sprite.Sprite):
    def __init__(self,filename,x,y,speed,angle,count=1,NotRadian=0,BombResist=0):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        x -= width/2
        y -= height/2
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        if NotRadian == 0:
            self.angle = math.radians(angle)
        elif NotRadian == 1:
            self.angle = angle
        if self.angle >= 360:
            self.angle -= 360
        self.speed = speed
        self.count = count
        self.delay = 0
        self.bflag = 0
        self.vx = math.cos(self.angle) *self.speed
        self.vy = math.sin(self.angle) *self.speed
        self.radius = (width/6) + (height/6)
        self.BombResist = BombResist
    def update(self):
        #self.rect.move_ip(self.rect.x,self.rect.y)
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = math.cos(self.angle) *self.speed
        self.vy = math.sin(self.angle) *self.speed

        self.delay -= 1
        if self.delay <= 0:
            self.bflag = 0
            self.delay = 0
        if self.bflag==0 and (self.count>0 or self.count ==-1):
            if self.rect.x <= -20:
                self.angle += math.radians(180)
                self.bflag = 1
                self.delay = 5
                self.count -= 1
            if self.rect.y <= -20:
                self.angle += math.radians(180)
                self.bflag = 1
                self.delay = 5
                self.count -= 1
            if self.rect.x >= 680:
                self.angle += math.radians(180)
                self.bflag = 1
                self.delay = 5
                self.count -= 1
            if self.rect.y >= 520:
                self.angle += math.radians(180)
                self.bflag = 1
                self.delay = 5
                self.count -= 1

        if(self.Pla.bombflag or self.Pla.BulletAnti) and self.BombResist == 0:
            self.kill()

        RectKill(self)

    def draw(self,screen):
        screen.blit(self.image.self.rect)

#分裂弾    ギミック:指定時間経過で、別の弾を打つ
#課題     どうやって、別クラスの弾を生成させるか
class BulletVanish(pygame.sprite.Sprite):
    def __init__(self,filename,x,y,speed,angle,time,bullet,filename2,vangle,count,NotRadian=0,VNotRadian=0,BombResist=0):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        x -= width/2
        y -= height/2
        self.x = x
        self.y = y
        self.width = width/2
        self.height = height/2
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        if NotRadian == 0:
            self.angle = math.radians(angle)
        if NotRadian == 1:
            self.angle = angle
        if self.angle >= 360:
            self.angle -= 360
        self.VNotRadian = VNotRadian
        self.speed = speed
        self.vx = math.cos(self.angle) *self.speed
        self.vy = math.sin(self.angle) *self.speed
        self.filename2 = filename2
        self.time = time
        self.resettime = time
        self.shotready = 0
        self.vangle = vangle
        self.count = count
        self.radius = (width/6) + (height/6)
        self.BombResist = BombResist
        self.bulletkill = bullet
    def update(self):
        #self.rect.move_ip(self.rect.x,self.rect.y)

        self.time -= 1

        if self.time <= 0:
            for i in range(0,self.count,1):
                BulletNormal(self.filename2,self.x+(self.width/2),self.y+(self.height/2),self.speed,self.vangle*i,self.VNotRadian)
            if self.bulletkill == 1:
                self.kill()
            else :
                self.time = self.resettime

        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y

        if (self.Pla.bombflag or self.Pla.BulletAnti) and self.BombResist == 0:
            self.kill()

        RectKill(self)

    def draw(self,screen):
        screen.blit(self.image.self.rect)

#ホーミング弾　ギミック：自機の方に向く
class BulletHorming(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, speed, angle, delay=120,timer=60,BombResist=0):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        x -= width / 2
        y -= height / 2
        self.x = x
        self.y = y
        self.rect = Rect(x, y, width, height)
        self.rect.center = (x / width, y / height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.angle = math.radians(angle) * 180 / math.pi
        self.delay = delay
        self.timer = timer
        self.speed = speed
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        self.radius = (width / 6) + (height / 6)
        self.timer = 120
        self.BombResist = BombResist
    def update(self):
        # self.rect.move_ip(self.rect.x,self.rect.y)
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y

        self.delay -= 1
        if self.delay <= 0:
            self.timer -= 1

        self.timer -= 1
        if (self.Pla.bombflag):
            self.kill()

        RectKill(self)

    def draw(self, screen):
        screen.blit(self.image.self.rect)

#重力弾　　ギミック：指定時間経過で徐々に下に傾く

class BulletGravity(pygame.sprite.Sprite):
    def __init__(self,filename,x,y,speed,angle,vangle,timer=60,NotRadian=0,BombResist=0):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        x -= width/2
        y -= height/2
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        if NotRadian == 0:
            self.angle = math.radians(angle)
        elif NotRadian == 1:
            self.angle = angle
        self.speed = speed
        self.timer = timer
        self.delay = 0
        self.bflag = 0
        self.vangle = vangle
        self.vx = math.cos(self.angle) *self.speed
        self.vy = math.sin(self.angle) *self.speed
        self.radius = (width/6) + (height/6)
        self.BombResist = BombResist

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = math.cos(self.angle) *self.speed
        self.vy = math.sin(self.angle) *self.speed

        self.timer -= 1

        if self.angle >= math.radians(360):
            self.angle -= math.radians(360)

        if self.timer <= 0:
            if self.angle > math.radians(90) and self.angle < math.radians(270):
                self.angle -= math.radians(self.vangle) / 10
            if self.angle >= math.radians(270) and self.angle <= math.radians(361):
                self.angle += math.radians(self.vangle) / 10
            if self.angle >= math.radians(0) and self.angle < math.radians(90):
                self.angle += math.radians(self.vangle) / 10

        if self.angle >= 360:
            self.angle -= 360

        if (self.Pla.bombflag or self.Pla.BulletAnti) and self.BombResist == 0:
            self.kill()

        RectKill(self)
    def draw(self):
        screen.blit(self.image,self.rect)

#------------------------------------------------------

#=プレイヤー専用の弾
class BulletPlayer(pygame.sprite.Sprite):
    def __init__(self,filename,x,y,speed,angle):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        x -= width/2
        y -= height/2
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.angle = math.radians(angle)
        self.speed = speed
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        self.Timer = 5
        self.radius = 1.5
    def update(self):
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y

        Ecollide = pygame.sprite.spritecollide(self,self.EHit,False,pygame.sprite.collide_circle)
        if Ecollide:
            self.Timer -= 2.5
        if self.Timer<= 0:
            self.kill()
        RectKill(self)
    def draw(self,screen):
        screen.blit(self.image.self.rect)

# PlayerClass

class PlayerJIKI(pygame.sprite.Sprite):
    def __init__(self,filename,x,y,Bomb=3,zanki=3):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.center = (x/width,y/height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = 0
        self.vy = 0
        self.speed = 3
        self.reload = 0
        self.radius = 3
        self.eraser = 0
        self.deathflag = 0
        self.hasbomb = Bomb
        self.zanki = zanki
        self.bombflag = 0
        self.bombtime = 180
        self.radius = 1
        self.invisibility = 1
        self.invisibletime = 180
        self.BulletAnti = 1
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx = 0
        self.vy = 0
        self.rect.x = self.x
        self.rect.y = self.y
        self.reload -= 1

        if self.invisibletime > 0:
            self.invisibletime -= 1

        if self.invisibletime == 0:
            self.invisibility = 0
            self.BulletAnti = 0

        if self.bombflag == 1:
            self.bombtime -= 1
            self.invisibility = 1
        if self.bombtime <= 0:
            self.bombflag = 0
            self.bombtime = 180
            self.invisibility = 0

        presskeys = pygame.key.get_pressed()
        if presskeys[K_LEFT]:
            self.vx = -self.speed
        if presskeys[K_RIGHT]:
            self.vx = self.speed
        if presskeys[K_UP]:
            self.vy = -self.speed
        if presskeys[K_DOWN]:
            self.vy = self.speed
        if presskeys[K_z]:
            if self.reload <= 0:
                PlayerShot(PlayerB,self.rect.x+6,self.rect.y+6,11,270)
                PlayerShot(PlayerB, self.rect.x + 16, self.rect.y + 6, 11, 270)
                self.reload = 4
        if presskeys[K_x] and self.bombflag==0 and self.hasbomb >= 1:
            if self.bombtime == 180:
                PBomb_sound.play()
            self.bombflag = 1
            self.hasbomb -= 1
        if presskeys[K_LSHIFT]:
            self.speed = 1

        else:
            self.speed = 3

        if self.x < -3:
            self.x = -2
        if self.x > 620:
            self.x = 619
        if self.y < -3:
            self.y = -2
        if self.y > 465:
            self.y = 464
        collide = pygame.sprite.spritecollide(self, self.EHit, False, pygame.sprite.collide_circle)
        if collide and self.invisibility == 0:
            Player_Hit_sound.play()
            self.deathflag = 1
            self.kill()

    def draw(self,screen):
        screen.blit(self.image,self.rect)

# 敵クラス
# Enemy Class

class TestEnemy(pygame.sprite.Sprite):
    def __init__(self,filename,x,y,vx,vy):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = vx
        self.vy = vy
        self.timer = 60
        self.speed = 2
        self.angle = 0
        self.HP = 2000
        self.GetPX = 0
        self.GetPY = 0
        self.PlayAngle = 0
        self.death = 0
        self.radius = (width/6) + (height/6)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y
        self.timer += 1
        self.GetPX = self.Pla.rect.x - self.x
        self.GetPY = self.Pla.rect.y - self.y
        self.PlayAngle = math.atan2(self.GetPY,self.GetPX)

        if self.timer >= 10:
            self.speed += 0.1
            if self.speed >= 5:
                self.speed = 0.1
            self.angle += 1
            #NormalShot(yellow1, self.rect.x+12,self.rect.y+12,self.speed,self.PlayAngle,1)
            #CurveShot(blue1,self.rect.x+12,self.rect.y+12,2,self.angle,31,120)
            #CurveShot2(red1,self.rect.x+12,self.rect.y+12,2,self.angle,40,45,9)
            #TurboShot(green1,self.rect.x+12,self.rect.y+12,1,self.angle,0.025)
            #TurboShot3(yellow2,self.rect.x+12,self.rect.y+12,2,self.angle,60,5,60,180,0,1)
            #TurboShot4(blue2,self.rect.x+12,self.rect.y+12,2,self.angle,5,60)
            #BoundShot(red2,self.rect.x+12,self.rect.y+12,2,self.angle,1)
            #VanishShot(yellow1,self.rect.x+12,self.rect.y+12,2,self.angle,120,0,red3,45,1)
            #NormalShot(blue1,self.rect.x+12,self.rect.y+12,2,0)
            self.timer = 0
        collide = pygame.sprite.spritecollide(self,self.Hit,False,pygame.sprite.collide_circle)
        if collide:
            self.HP -= ShotDamage
        if self.HP <= 0:
            ItemBomb(self.rect.x,self.rect.y)
            Item1UP(self.rect.x,self.rect.y-20)
            ScoreI10000(self.rect.x,self.rect.y)
            ScoreI10000(self.rect.x+20,self.rect.y-10)
            ScoreI10000(self.rect.x-20,self.rect.y-10)
            self.rect.x = -4096
            self.rect.y = -4096
            shoot_sound.play()
            self.kill()
            #if self.Pla.bombflag:
            #    self.HP +=640
        if self.Pla.bombflag:
            self.HP -= 300
        if self.HP >= 2000:
            self.HP = 2000

    def draw(self,screen):
        screen.blit(self.image, self.rect)

class Enemy1(pygame.sprite.Sprite):
    def __init__(self,x,y,HP,pattern=0,delay=0):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(zako1).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.x = self.y
        self.vx = 0
        self.vy = 0
        self.HP = HP
        self.delay = delay
        self.PlayerAngle = 0
        self.mtimer = -180
        self.timer = 0
        self.radius = (width/6) + (height/6)
        self.pattern = pattern

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y
        self.GetPX = self.Pla.rect.x - self.x
        self.GetPY = self.Pla.rect.y - self.y

        if self.delay > 1:
            self.delay -= 1
            self.mtimer = -180
            self.timer = 0

        self.mtimer += 1
        self.PlayerAngle = math.atan2(self.GetPY,self.GetPX)

        if self.mtimer >= 0 and self.mtimer <= 180:
            self.vy = 1
        else :
            self.vy = 0
        if self.mtimer >= 720:
            self.vy = -1
        if self.mtimer >= 960:
            self.kill()

        self.timer += 1

        if self.timer == 180:
            if self.pattern == 0:
                for i in range(0,3,1):
                    NormalShot(red1,self.x+6,self.y+16,2,math.atan2(self.Pla.rect.centery - (self.y + 16),self.Pla.rect.centerx - (self.x + 6))+0.3*i,1)
            if self.pattern == 1:
                for i in range(0,10,1):
                    NormalShot(blue1,self.x+6,self.y+16,random.randint(1,9)*0.25,random.randint(75,105),0)
            if self.pattern == 2:
                for i in range(1,5,1):
                    NormalShot(green1,self.x+6,self.y+16,1*i,math.atan2(self.Pla.rect.centery - (self.y + 16),self.Pla.rect.centery- (self.x + 6)),1)
            if self.pattern == 3:
                for i in range(0,360,45):
                    NormalShot(yellow1,self.x+6,self.y+16,2,i,0)
            if self.pattern == 4:
                for i in range(0,180,30):
                    TurboShot(green3,self.x,self.y,2,i,0.25,0,1)
            self.timer = 0

        collide = pygame.sprite.spritecollide(self,self.Hit,True,pygame.sprite.collide_circle)
        if collide and self.delay <= 0:
            self.HP -= ShotDamage
        if self.Pla.bombflag and self.delay <= 0:
            self.HP -= 300
        if self.HP <= 0:
            shoot_sound.play()
            self.kill()

    def draw(self,screen):
        screen.blit(self.image,self.rect)

class Enemy2(pygame.sprite.Sprite):
    def __init__(self,x,y,HP,pattern = 0,delay=0):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(zako3).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.x = self.y
        self.vx = 0
        self.vy = 0
        self.HP = HP
        self.delay = delay
        self.PlayerAngle = 0
        self.mtimer = -1
        self.timer = 0
        self.reload = 0
        self.radius = (width/6) + (height/6)
        self.pattern = pattern

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y
        self.GetPX = self.Pla.rect.x - self.x
        self.GetPY = self.Pla.rect.y - self.y

        if self.delay > 0:
            self.delay -= 1
            self.mtimer = -1
            self.timer = 0

        self.mtimer += 1
        self.timer += 1
        if self.mtimer >= 1:
            self.vy = 1

        if self.timer >= 30:
            if self.pattern == 0:
                self.reload += 1
                if self.reload == 5:
                    NormalShot(yellow1,self.x+12,self.y+24,2,90,0,0)
                    self.reload = 0
            if self.pattern == 1:
                self.reload += 1
                if self.reload == 4:
                    CurveShot(green2,self.x+12,self.y+24,2,random.randint(0,360),0.5,120,0,0)
                    self.reload = 0
        if self.timer >= 60:
            self.timer = 0

        collide = pygame.sprite.spritecollide(self,self.Hit,True,pygame.sprite.collide_circle)
        if collide and self.delay <= 0:
            self.HP -= ShotDamage
        if self.Pla.bombflag and self.delay <= 0:
            self.HP -= 300
        if self.HP <= 0:
            shoot_sound.play()
            self.kill()

    def draw(self,screen):
        screen.blit(self.image,self.rect)

class Stage1MBoss(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(Boss1).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = 0
        self.vy = 0
        self.speed = 1
        self.HP = 5000
        self.Phaze = 0
        self.delay = 120
        self.timer = 0
        self.ftimer = 0
        self.escapewait = 0
        self.radius = (width/6) + (height/6)
        self.angle = 0
        self.moveangle = math.radians(90)
        self.HPMAX = self.HP
        self.invisible = self.delay
        self.pattern = 0

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy = math.sin(self.moveangle)*self.speed
        self.vx = math.cos(self.moveangle)*self.speed
        self.rect.x = self.x
        self.rect.y = self.y
        #self.GetPX = self.Pla.rect.x - self.x
        #self.GetPY = self.Pla.rect.y - self.y
        if self.delay > 0:
            self.delay -= 1
            self.invisible -= 1
        if self.delay <= 0:
            self.timer += 1
            self.speed = 0
        collide = pygame.sprite.spritecollide(self,self.Hit,False,pygame.sprite.collide_circle)

        if self.Phaze == 0: #第一段階
            if self.timer >= 60 and self.timer <= 60*3:
                self.moveangle = math.radians(45)
                self.speed = 1
                self.ftimer += 1
                if self.ftimer >= 5:
                    NormalShot(red1,self.x+56,self.y+48,2,math.atan2(self.Pla.rect.centery-(self.y+48),self.Pla.rect.centerx-(self.x+56)),1,0)
                    self.ftimer = 0
            if self.timer >= 60*4 and self.timer <= 60*6:
                self.moveangle = math.radians(-135)
                self.speed = 1
                self.ftimer += 1
                if self.ftimer == 10:
                    i = 0
                    while i<30:
                        NormalShot(blue1,self.x+56,self.y+48,2,(12*i)+i,0,0)
                        i += 1
                    self.ftimer = 0
            if self.timer >= 60*7 and self.timer <= 60*9:
                self.moveangle = math.radians(135)
                self.speed = 1
                self.ftimer += 1
                if self.ftimer >= 5:
                    NormalShot(red1,self.x+56,self.y+48,2,math.atan2(self.Pla.rect.centery-(self.y+48),self.Pla.rect.centerx-(self.x+56)),1,0)
                    self.ftimer = 0
            if self.timer >= 60*10 and self.timer <= 60*12:
                self.moveangle = math.radians(-45)
                self.speed = 1
                self.ftimer += 1
                if self.ftimer >= 10:
                    i = 0
                    while i<30:
                        NormalShot(blue1,self.x+56,self.y+48,2,(-12*i)-i,0,0)
                        i += 1
                    self.ftimer = 0
            if self.timer == 60*13:
                self.timer = 0
        #ここまで-----------------------------------------
        if self.Phaze == 1: #第2段階
            if self.pattern == 0 and not((self.x >= 0 and self.x <= 16) and (self.y >= 76 and self.y <= 96)):
                self.moveangle = math.atan2(80-self.y,0-self.x)
                self.speed = 4
                self.timer = 0
            else :
                self.speed = 0
                self.pattern = 1
            if self.timer >= 60 and self.timer <= 60*4:
                self.speed = 3
                self.moveangle = math.radians(0)
                self.ftimer += 1
                if self.ftimer == 5:
                    NormalShot(yellow1,self.x+16,self.y+47,3,90,0,0)
                    self.ftimer = 0
            if self.timer >= 60*5 and self.timer <= 60*8:
                self.speed = 3
                self.moveangle = math.radians(180)
                self.ftimer += 1
                if self.ftimer == 5:
                    NormalShot(yellow1, self.x+96, self.y+47, 3, 90, 0, 0)
                    self.ftimer = 0
            if self.timer == 60*9:
                self.speed = 0
                self.moveangle = 0
                self.timer = 0
                self.ftimer = 0
            #ここまで----------------------------------------
        if collide and self.HP >= 1 and self.invisible <= 0:
            self.HP -= ShotDamage
        if self.Pla.bombflag:
            self.HP -= 8
        if self.HP <= 2500:
            if self.Phaze == 0:
                shoot_sound.play()
                self.mtimer = 0
                self.timer = 0
                self.Phaze = 1
        if self.HP <= 0:
            self.escapewait += 1
            self.timer = -60
            self.ftimer = -60
        if self.escapewait >= 180:
            self.vy = -3
        if self.escapewait == 180:
            ItemScore2000(self.x+56,self.y+48)
            ItemScore2000(self.x+24,self.y+30)
            ItemScore2000(self.x+1,self.y+14)
            ItemScore2000(self.x+40,self.y+30)
            ItemScore2000(self.x+34,self.y+22)
        if self.escapewait == 360:
            self.kill()

    def draw(self,screen):
        screen.blit(self.image,self.rect)

class Stage1boss(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(Boss1).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = 0
        self.vy = 0
        self.speed = 2
        self.HP = 7500
        self.Phaze = 0
        self.Phaze1angle = 0
        self.delay = 120
        self.timer = -121
        self.ftimer = 0
        self.ftimer2 = 0
        self.mtimer = 0
        self.escapewait = 0
        self.radius = (width/6) + (height/6)
        self.angle = 0
        self.moveangle = math.radians(90)
        self.HPMAX = self.HP
        self.invisible = self.delay
        self.pattern = -1

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy = math.sin(self.moveangle)*self.speed
        self.vx = math.cos(self.moveangle)*self.speed
        self.rect.x = self.x
        self.rect.y = self.y

        if self.delay > 0:
            self.delay -= 1
            self.invisible -= 1
        elif self.delay <= 0:
            self.speed = 0
            self.timer += 1
            self.mtimer += 1

        if self.x < -6:
            self.x = -5
        if self.x > 540:
            self.x = 539

        #移動行動

        #第一段階
        if self.mtimer == 1 and self.Phaze == 0:
            if self.x >= self.Pla.x:
                self.moveangle = math.radians(180)
            if self.x < self.Pla.x:
                self.moveangle = math.radians(0)
        if self.mtimer >= 10 and self.Phaze == 0:
            self.speed = 2
        if self.mtimer >= 60 and self.Phaze == 0:
            self.mtimer = 0

        #第二段階
        if (self.mtimer >= -60 and self.mtimer < 0) and self.Phaze == 1:
            self.moveangle = math.atan2(80-self.y,320-self.x)
            self.speed = 4
        if self.mtimer == 0 and self.Phaze == 1:
            self.moveangle = math.radians(0)
            self.speed = 1

        #--------------------------------------------

        #登場
        if self.timer >= -120 and self.timer < 0 and self.pattern == -1:
            self.moveangle = math.radians(270)
            self.speed = 0.5
            self.ftimer += 1
            if self.ftimer >= 2:
                for i in range(0,3,1):
                    self.Phaze1angle += 5
                    NormalShot(red1,self.x+56,self.y+48,2,self.Phaze1angle+(i*120),0,0)
                self.ftimer = 0
        if self.timer == 0 and self.pattern == -1:
            self.pattern = 0

        #攻撃行動
        # 第一段階
        if self.Phaze == 0:
            if self.timer >= 30 and self.timer <= 180:
                self.ftimer += 1
                if self.ftimer == 10:
                    NormalShot(green2,self.x+45,self.y+96,3,90,0,0)
                    NormalShot(green2, self.x + 68, self.y + 96, 3, 90, 0, 0)
                    self.ftimer = 0
            if self.timer >= 180 and self.timer <= 360:
                self.ftimer += 1
                if self.ftimer == 15:
                    VanishShot(red3,self.x+15,self.y+100,2,90,60,1,red1,30,15,0,0,0)
                if self.ftimer == 30:
                    VanishShot(red3f,self.x+90, self.y+100, 2,90, 60, 1, red1, 30+random.randint(-20,20), 15, 0, 0, 0)
                    self.ftimer = 0
            if self.timer >= 360:
                self.timer = 0
                self.ftimer = 0
        # 第二段階
        if self.Phaze == 1:
            if self.timer >= 0 and self.timer < 300:
                self.ftimer += 1
                if self.ftimer == 8:
                    NormalShot(blue2,self.x+95,self.y+50,2,random.randint(75,115),0,0)
                    NormalShot(blue2,self.x+20,self.y+50,2,random.randint(75,115),0,0)
                    self.ftimer = 0
            if self.timer >= 240 and self.timer < 300:
                self.ftimer2 += 1
                if self.ftimer2 == 60:
                    self.Phaze1angle += 1
                    for i in range(1,4,1):
                        for j in range(0,6,1):
                            NormalShot(red3,self.x+15,self.y+100,2*i*0.5,(35*j)+self.Phaze1angle,0,0)
                            NormalShot(red3,self.x+90,self.y+100,2*i*0.5,(35*j)+self.Phaze1angle,0,0)
                            self.ftimer2 = 0
            if self.timer >= 300:
                self.timer = 0

        #--------------------------------------------

        if self.HP <=5000 and self.Phaze == 0:
            ScoreI10000(self.x+64,self.y+64)
            ScoreI10000(self.x+-32,self.y+32)
            ScoreI10000(self.x+96,self.y+32)
            self.timer = -60
            self.ftimer = 0
            self.mtimer = -60
            self.Phaze = 1
            self.Phaze1angle = 0
        if self.HP <= 0:
            self.kill()

        collide = pygame.sprite.spritecollide(self,self.Hit,False,pygame.sprite.collide_circle)
        if collide:
            self.HP -= ShotDamage
        if self.HP <= 0:
            shoot_sound.play()
            self.kill()

    def draw(self,screen):
        screen.blit(self.image,self.rect)

class ScoreEnemy100(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(Menemy100).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = 0
        self.vy = 0
        self.HP = 500
        self.radius = (width/6) + (height/6)

    def update(self):
        self.x += self.vx
        self.y += self.vy

        if self.HP <= 0:
            ScoreI100(self.rect.x,self.rect.y)
            self.kill()

        collide = pygame.sprite.spritecollide(self,self.Hit,False,pygame.sprite.collide_circle)
        if collide:
            self.HP -= ShotDamage
        if self.HP <= 0:
            ScoreI100(self.rect.x,self.rect.y)
            self.kill()

    def draw(self,screen):
        screen.blit(self.image,self.rect)

class ScoreEnemy300(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(Menemy300).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = 0
        self.vy = 0
        self.HP = 750
        self.radius = (width/6) + (height/6)

    def update(self):
        self.x += self.vx
        self.y += self.vy

        collide = pygame.sprite.spritecollide(self,self.Hit,False,pygame.sprite.collide_circle)
        if collide:
            self.HP -= ShotDamage
        if self.HP <= 0:
            ScoreI300(self.rect.x,self.rect.y)
            self.kill()

    def draw(self,screen):
        screen.blit(self.image,self.rect)

class ScoreEnemy500(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(Menemy500).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = 0
        self.vy = 0
        self.HP = 1250
        self.radius = (width/6) + (height/6)

    def update(self):
        self.x += self.vx
        self.y += self.vy

        collide = pygame.sprite.spritecollide(self,self.Hit,False,pygame.sprite.collide_circle)
        if collide:
            self.HP -= ShotDamage
        if self.HP <= 0:
            ScoreI500(self.rect.x,self.rect.y)
            self.kill()

    def draw(self,screen):
        screen.blit(self.image,self.rect)

class ScoreEnemy5000(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(Menemy5000).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = 0
        self.vy = 0
        self.HP = 1500
        self.radius = (width/6) + (height/6)

    def update(self):
        self.x += self.vx
        self.y += self.vy

        collide = pygame.sprite.spritecollide(self,self.Hit,False,pygame.sprite.collide_circle)
        if collide:
            self.HP -= ShotDamage
        if self.HP <= 0:
            ScoreI5000(self.rect.x,self.rect.y)
            self.kill()

    def draw(self,screen):
        screen.blit(self.image,self.rect)

class ScoreEnemy10000(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(Menemy10000).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = 0
        self.vy = 0
        self.HP = 3500
        self.radius = (width/6) + (height/6)

    def update(self):
        self.x += self.vx
        self.y += self.vy

        collide = pygame.sprite.spritecollide(self,self.Hit,False,pygame.sprite.collide_circle)
        if collide:
            self.HP -= ShotDamage
        if self.HP <= 0:
            ScoreI10000(self.rect.x,self.rect.y)
            self.kill()

    def draw(self,screen):
        screen.blit(self.image,self.rect)

'''
class ScoreEnemy(pygame.sprite.Sprite):
    def __init__(self,x,y,Value=0):
        self.MenemySG = [Menemy100,Menemy300,Menemy500,Menemy5000,Menemy10000]
        self.SItem = [0,1,2,3,5,6]
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load(self.MenemySG[Value]).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x,y,width,height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = 0
        self.vy = 0
        self.ScoreItem = Value

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self,screen):
        screen.blit(self.image,self.rect)
'''

def RectKill(BSprite):
    if BSprite.rect.x <= -40:
        BSprite.kill()
    if BSprite.rect.y <= -40:
        BSprite.kill()
    if BSprite.rect.x >= 700:
        BSprite.kill()
    if BSprite.rect.y >= 540:
        BSprite.kill()
    return 0


if __name__ == "__main__":
    MainGame()
