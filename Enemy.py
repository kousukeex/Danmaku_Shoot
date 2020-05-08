import pygame
from EnemyBullet import *
from Items import *
from pygame.locals import *
from imglibrary import *
from common import ScoreData
import random


# 敵
# スーパークラス
class Enemy(pygame.sprite.Sprite):
    containers = None
    hit_damage = 10
    player = None
    player_bullet_group = None
    shoot_sound = None

    def __init__(self, x, y, hp, delay, score=0,enable_suicide=False):
        pygame.sprite.Sprite.__init__(self, Enemy.containers)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x
        self.y = y
        self.hp = hp
        self.delay = delay
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.rect.x = self.x
        self.rect.x = self.y
        self.vx = 0
        self.vy = 0
        self.move_timer = -1
        self.timer = 0
        self.reload = 0
        self.radius = (self.width / 6) + (self.height / 6)
        self.score = score
        self.enable_suicide = enable_suicide

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y
        self.move()
        self.action()
        self.hit_check()

    def move(self):
        self.move_timer += 1
        if self.delay > 0:
            self.delay -= 1
            self.move_timer = -1
            self.timer = 0

    def action(self):
        self.timer += 1

    def hit_check(self):
        collide = pygame.sprite.spritecollide(self, Enemy.player_bullet_group, True, pygame.sprite.collide_circle)
        if collide and self.delay == 0:
            self.hp -= Enemy.hit_damage
            ScoreData.add_score(Enemy.hit_damage)
        if Enemy.player.bomb_flag and self.delay <= 0:
            self.hp -= 2
        if self.enable_suicide and Enemy.player.invisibility:
            self.death(False)
        elif self.hp <= 0:
            self.death(True)

    def death(self, is_shoot):
        #Enemy.shoot_sound.play()
        if is_shoot:
            ScoreData.add_score(self.score)
        self.kill()

    def draw(self, screen):
        screen.blit(self.image.self.rect)

    @classmethod
    def registry(cls, *groups):
        Enemy.containers = groups

    @classmethod
    def player_registry(cls,player):
        cls.player = player

    @classmethod
    def player_bullet_group_registry(cls,group):
        cls.player_bullet_group = group

    @classmethod
    def shoot_sound_registry(cls,sound):
        cls.shoot_sound = sound

# スーパークラス
class Enemy1(Enemy):
    def __init__(self, x, y, hp, pattern=0, delay=0):
        self.image = pygame.image.load(zako1).convert_alpha()
        super().__init__(x, y, hp, delay, 100,True)
        self.pattern = pattern

    def update(self):
        super().update()

    def move(self):
        super().move()
        if 0 <= self.move_timer and self.move_timer <= 180:
            self.vy = 1
        else:
            self.vy = 0
        if self.move_timer >= 720:
            self.vy = -1
        if self.move_timer >= 960:
            self.kill()

    def action(self):
        super().action()
        self.pattern_action()

    def pattern_action(self):
        if self.pattern == 0:
            if self.timer == 180:
                for i in range(-1, 2, 1):
                    BulletNormal(red1,
                                 self.x + 6,
                                 self.y + 16,
                                 2,
                                 Enemy.player.get_player_angle(self.x + 6, self.y + 16) + 0.3 * i,
                                 0,
                                 False)
                self.timer = 0
        if self.pattern == 1:
            if self.timer == 90:
                for i in range(0, 10, 1):
                    BulletNormal(blue1,
                                 self.x + 6,
                                 self.y + 16,
                                 random.randint(1, 9) * 0.25,
                                 random.randint(75, 105),
                                 0,
                                 True)
                self.timer = 0
        if self.pattern == 2:
            if self.timer == 120:
                for i in range(1, 5, 1):
                    BulletNormal(green1,
                                self.x + 6,
                                self.y + 16,
                                1 * i,
                                Enemy.player.get_player_angle(self.x, self.y),
                                0,
                                False)
                self.timer = 0
        if self.pattern == 3:
            if self.timer == 80:
                for i in range(0, 360, 45):
                    BulletNormal(yellow1, self.x + 6, self.y + 16, 2, i, 0, True)
                self.timer = 0
        if self.pattern == 4:
            if self.timer == 40:
                for i in range(0, 180, 30):
                    BulletTurbo(green3, self.x, self.y, 2, i,
                            0,5,False,False)
                self.timer = 0


class Enemy2(Enemy):
    def __init__(self, x, y, hp, pattern=0, delay=0):
        self.image = pygame.image.load(zako3).convert_alpha()
        super().__init__(x, y, hp, delay, 50,True)
        self.reload = 0
        self.pattern = pattern

    def update(self):
        if self.y >= 510:
            self.kill()
        super().update()


    def move(self):
        if self.move_timer >= 1:
            self.vy = 1

    def action(self):
        if self.timer >= 30:
            self.pattern_action()
        if self.timer >= 60:
            self.timer = 0

    def pattern_action(self):
        if self.pattern == 0:
            self.reload += 1
            if self.reload == 5:
                BulletNormal(yellow1, self.x + 12, self.y + 24, 2, 90, 0, False)
                self.reload = 0
        if self.pattern == 1:
            self.reload += 1
            if self.reload == 4:
                BulletCurve(green2, self.x + 12, self.y + 24, 2, random.randint(0, 360), 0.5, 120, 0, False)
                self.reload = 0


class Stage1MBoss(Enemy):
    def __init__(self, x, y):
        self.image = pygame.image.load(Boss1).convert_alpha()
        super().__init__(x, y, 5000, 120)
        self.speed = 1
        self.hp = 5000
        self.phase = 1
        self.delay = 120
        self.timer = 0
        self.fire_timer = 0
        self.escape = 0
        self.angle = 0
        self.move_angle = math.radians(90)
        self.max_hp = self.hp
        self.invisible_time = 120
        self.pattern = 0

    def move(self):
        self.vy = math.sin(self.move_angle) * self.speed
        self.vx = math.cos(self.move_angle) * self.speed
        super().move()
        self.phase_move()
        self.escape_move()

    def phase_move(self):
        if self.phase == 1:
            if self.delay <= 0:
                self.speed = 0
            if 60 <= self.move_timer and self.move_timer <= 180:
                self.move_angle = math.radians(45)
                self.speed = 1
            if 240 <= self.move_timer and self.move_timer <= 360:
                self.move_angle = math.radians(-135)
                self.speed = 1
            if 420 <= self.move_timer and self.move_timer <= 540:
                self.move_angle = math.radians(135)
                self.speed = 1
            if 600 <= self.move_timer and self.move_timer <= 720:
                self.move_angle = math.radians(-45)
                self.speed = 1
            if self.move_timer == 780:
                self.move_timer = 0
        if self.phase == 2:
            if self.pattern == 0 and not ((0 <= self.x and self.x <= 16) and (76 <= self.y and self.y <= 96)):
                self.move_angle = math.atan2(80 - self.y, 0 - self.x)
                self.speed = 4
                self.timer = 0
            else:
                self.speed = 0
                self.pattern = 1
            if 60 <= self.move_timer and self.move_timer < 240:
                self.speed = 3
                self.move_angle = math.radians(0)
            if 240 <= self.move_timer and self.move_timer <= 299:
                self.speed = 0
            if 300 <= self.move_timer and self.move_timer < 480:
                self.speed = 3
                self.move_angle = math.radians(180)
            if self.move_timer == 480:
                self.speed = 0
            if self.move_timer == 540:
                self.move_timer = 0

    def escape_move(self):
        if self.escape >= 180:
            self.vy = -3

    def action(self):
        super().action()
        self.phase_action()

    def phase_action(self):
        if self.phase == 1:
            if self.timer >= 60 and self.timer <= 180:
                self.fire_timer += 1
                if self.fire_timer >= 5:
                    BulletNormal(red1,
                                 self.x + 56,
                                 self.y + 48,
                                 2,
                                 Enemy.player.get_player_angle(self.x + 56, self.y + 48),
                                 0,
                                 False
                                 )
                    self.fire_timer = 0
            if 240 <= self.timer and self.timer <= 360:
                self.fire_timer += 1
                if self.fire_timer == 10:
                    for i in range(0, 30, 1):
                        BulletNormal(blue1,
                                     self.x + 56,
                                     self.y + 48,
                                     2,
                                     (12 * i) + i,
                                     0,
                                     False)
                    self.fire_timer = 0
            if 420 <= self.timer and self.timer <= 540:
                self.fire_timer += 1
                if self.fire_timer >= 5:
                    BulletNormal(red1, self.x + 56, self.y + 48, 2,
                                 Enemy.player.get_player_angle(self.x + 56, self.y + 48),
                                 0,
                                 False)
                    self.fire_timer = 0
            if 600 <= self.timer and self.timer <= 720:
                self.fire_timer += 1
                if self.fire_timer == 10:
                    for i in range(0, 30, 1):
                        BulletNormal(blue1, self.x + 56, self.y + 48, 2, (-12 * i) - i, 0, False)
                    self.fire_timer = 0
            if self.timer == 780:
                self.timer = 0
        if self.phase == 2:
            self.fire_timer += 1
            if self.fire_timer == 15:
                BulletNormal(yellow1, self.x + 16, self.y + 47, 3, 90, 0, True)
                BulletNormal(yellow1, self.x + 96, self.y + 47, 3, 90, 0, True)
                self.fire_timer = 0

    def update(self):
        super().update()
        if self.delay == -119:
            Enemy.player.set_invisibility(120)
        if self.delay > 0:
            self.invisible_time -= 1
        self.hp_check()

    def hp_check(self):
        if self.hp <= 2500:
            if self.phase == 1:
                #Enemy.shoot_sound.play()
                self.move_timer = 0
                self.timer = 0
                self.fire_timer = -5
                self.phase = 2
        if self.hp <= 0:
            self.escape += 1
            self.timer = 0
            self.move_timer = 0
            self.fire_timer = -60

    def death(self,is_shoot=True):
        if self.escape == 180:
            ItemScore2000(self.x + 56, self.y + 48)
            ItemScore2000(self.x + 24, self.y + 30)
            ItemScore2000(self.x + 1, self.y + 14)
            ItemScore2000(self.x + 40, self.y + 30)
            ItemScore2000(self.x + 34, self.y + 22)
        if self.escape == 360:
            self.kill()


class Stage1boss(Enemy):
    def __init__(self, x, y):
        self.image = pygame.image.load(Boss1).convert_alpha()
        super().__init__(x, y, 7500, 0)
        self.speed = 2
        self.Phaze = 1
        self.Phaze1angle = 0
        self.timer = -120
        self.ftimer = 0
        # self.ftimer2 = 0
        self.move_timer = -120
        self.escapewait = 0
        self.angle = 0
        self.moveangle = math.radians(90)
        self.max_hp = self.hp
        self.invisible = self.delay
        self.entered = False

    def move(self):
        self.vy = math.sin(self.moveangle) * self.speed
        self.vx = math.cos(self.moveangle) * self.speed
        super().move()
        if not self.entered:
            if self.move_timer < 0:
                self.moveangle = math.radians(90)
                self.speed = 2
            if 0 <= self.move_timer and self.move_timer <= 120:
                self.moveangle = math.radians(270)
                self.speed = 0.5
            if self.move_timer >= 120:
                self.move_timer = 0
                self.entered = True
        self.phase_move()

    def phase_move(self):
        print(self.move_timer)
        if self.Phaze == 1 and self.entered:
            if self.move_timer == 1:
                if self.x >= Enemy.player.x:
                    self.moveangle = math.radians(180)
                if self.x < Enemy.player.x:
                    self.moveangle = math.radians(0)
            if 0 <= self.move_timer and self.move_timer <= 9:
                self.speed = 0
            if 10 <= self.move_timer and self.move_timer <= 59:
                self.speed = 2
            if 60 <= self.move_timer:
                self.move_timer = 0
        if self.Phaze == 2:
            if -60 <= self.move_timer and self.move_timer < 0:
                self.moveangle = math.atan2(80 - self.y, 320 - self.x)
                self.speed = 4
            if self.move_timer == 0:
                self.speed = 0

    def action(self):
        super().action()
        if not self.entered:
            if self.timer == -119:
                Enemy.player.set_invisibility(60)
            if 0 <= self.timer and self.timer <= 120:
                self.ftimer += 1
                if self.ftimer >= 2:
                    for i in range(0, 3, 1):
                        self.Phaze1angle += 5
                        BulletNormal(red1, self.x + 56, self.y + 48, 2, self.Phaze1angle + (i * 119), 0, True)
                    self.ftimer = 0
        self.phase_action()

    def phase_action(self):
        if self.Phaze == 1 and self.entered:
            if 30 <= self.timer and self.timer <= 180:
                self.ftimer += 1
                if self.ftimer == 10:
                    BulletNormal(green2, self.x + 45, self.y + 96, 3, 90, 0, True, False)
                    BulletNormal(green2, self.x + 68, self.y + 96, 3, 90, 0, True, False)
                    self.ftimer = 0
            if 180 <= self.timer and self.timer <= 360:
                self.ftimer += 1
                if self.ftimer == 15:
                    BulletVariance(red3, self.x + 15, self.y + 100, 2, math.radians(90), 60, 15, red1, 30, False, False,
                                   False, True)
                if self.ftimer == 30:
                    BulletVariance(red3, self.x + 90, self.y + 100, 2, math.radians(90), 60, 15, red1, 30, False, False,
                                   False, True)
                    self.ftimer = 0
            if self.timer >= 360:
                self.timer = 0
                self.ftimer = 0
        if self.Phaze == 2:
            if 0 <= self.timer and self.timer < 300:
                self.ftimer += 1
                if self.ftimer == 8:
                    BulletNormal(blue2, self.x + 95, self.y + 50, 2, random.randint(75, 115), 0, 0)
                    BulletNormal(blue2, self.x + 20, self.y + 50, 2, random.randint(75, 115), 0, 0)
                    self.ftimer = 0
            if 300 <= self.timer:
                self.Phaze1angle += 1
                for i in range(1, 4, 1):
                    for j in range(0, 12, 1):
                        BulletNormal(red3, self.x + 15, self.y + 100, 2 * i * 0.5,
                                     (30 * j) + self.Phaze1angle, 0, True, False)
                        BulletNormal(red3, self.x + 90, self.y + 100, 2 * i * 0.5,
                                     (30 * j) + self.Phaze1angle, 0, True, False)
                self.timer = 0

    def update(self):
        super().update()

        if self.delay > 0:
            self.invisible -= 1
        if self.x < -6:
            self.x = -5
        if self.x > 540:
            self.x = 539

        if self.hp <= 5000 and self.Phaze == 1:
            ItemScore10000(self.x + 64, self.y + 64)
            ItemScore10000(self.x + -32, self.y + 32)
            ItemScore10000(self.x + 96, self.y + 32)
            self.timer = -60
            self.ftimer = 0
            self.move_timer = -60
            self.Phaze = 2
            self.Phaze1angle = 0

        if self.hp <= 0:
            ItemScore10000(self.x + 64, self.y + 64)
            ItemScore10000(self.x + -32, self.y + 32)
            ItemScore10000(self.x + 96, self.y + 32)
            ItemScore10000(self.x + 32, self.y + 64)
            ItemScore10000(self.x + -32, self.y + 32)
            ItemScore10000(self.x + 96, self.y + 32)
            ItemScore10000(self.x + 128, self.y + 64)
            ItemScore10000(self.x + -32, self.y + 32)
            ItemScore10000(self.x + 96, self.y + 32)
            self.kill()


class TestEnemy(Enemy):
    def __init__(self, filename, x, y, vx, vy):
        pygame.sprite.Sprite.__init__(self, TestEnemy.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x, y, width, height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = vx
        self.vy = vy
        self.timer = 60
        self.speed = 2
        self.angle = 0
        self.hp = 2000
        self.GetPX = 0
        self.GetPY = 0
        self.playeryAngle = 0
        self.death = 0
        self.radius = (width / 6) + (height / 6)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y
        self.timer += 1
        self.GetPX = Enemy.player.rect.x - self.x
        self.GetPY = Enemy.player.rect.y - self.y
        self.PlayAngle = math.atan2(self.GetPY, self.GetPX)

        if self.timer >= 10:
            self.speed += 0.1
            if self.speed >= 5:
                self.speed = 0.1
            self.angle += 1
            # NormalShot(yellow1, self.rect.x+12,self.rect.y+12,self.speed,self.PlayAngle,1)
            # CurveShot(blue1,self.rect.x+12,self.rect.y+12,2,self.angle,31,120)
            # CurveShot2(red1,self.rect.x+12,self.rect.y+12,2,self.angle,40,45,9)
            # TurboShot(green1,self.rect.x+12,self.rect.y+12,1,self.angle,0.025)
            # TurboShot3(yellow2,self.rect.x+12,self.rect.y+12,2,self.angle,60,5,60,180,0,1)
            # TurboShot4(blue2,self.rect.x+12,self.rect.y+12,2,self.angle,5,60)
            # BoundShot(red2,self.rect.x+12,self.rect.y+12,2,self.angle,1)
            # VanishShot(yellow1,self.rect.x+12,self.rect.y+12,2,self.angle,120,0,red3,45,1)
            # NormalShot(blue1,self.rect.x+12,self.rect.y+12,2,0)
            self.timer = 0
        collide = pygame.sprite.spritecollide(self, self.Hit, False, pygame.sprite.collide_circle)
        if collide:
            self.hp -= Enemy.hit_damage
        if self.hp <= 0:
            # ItemBomb(self.rect.x, self.rect.y)
            # Item1UP(self.rect.x, self.rect.y - 20)
            ItemScore10000(self.rect.x, self.rect.y)
            ItemScore10000(self.rect.x + 20, self.rect.y - 10)
            ItemScore10000(self.rect.x - 20, self.rect.y - 10)
            self.rect.x = -4096
            self.rect.y = -4096
            # Enemy.shoot_sound.play()
            self.kill()
            # if self.Pla.bombflag:
            #    self.hp +=640
        if Enemy.player.bombflag:
            self.hp -= 300
        if self.hp >= 2000:
            self.hp = 2000

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class ScoreEnemy100(Enemy):
    def __init__(self, x, y):
        self.image = pygame.image.load(Menemy100).convert_alpha()
        self.reload = 0
        super().__init__(x, y, 100, 0, 100)

    def update(self):
        super().update()
        if self.y >= 510:
            self.kill()

    def move(self):
        self.vy = 1

    def action(self):
        super().action()
        if self.timer == 50:
            self.reload += 1
            for x in range(random.randint(1,10), 360, 30):
                BulletNormal(yellow1, self.x + 32, self.y + 32, 1.5, x, 5, True, False)
            self.timer = 0
        if self.reload == 3:
            BulletTurbo(yellow3, self.x + 32, self.y + 32, 1, Enemy.player.get_player_angle(self.x - 32, self.y - 32),
                        10, 0.5, False, False)
            self.reload = 0

    def death(self,is_shoot):
        super().death(is_shoot)
        if is_shoot:
            ItemScore100(self.x + 32, self.y + 32)
        BulletNormal(yellow3, self.x + 32, self.y + 32, 3, Enemy.player.get_player_angle(self.x - 32, self.y - 32),
                     False, False)


class ScoreEnemy300(Enemy):
    def __init__(self, x, y):
        self.image = pygame.image.load(Menemy300).convert_alpha()
        self.angle = 0
        super().__init__(x, y, 300, 0, 300)

    def update(self):
        super().update()
        if self.y >= 510:
            self.kill()

    def move(self):
        self.vy = 1

    def action(self):
        super().action()
        if self.timer == 4:
            BulletNormal(green1, self.x + 32, self.y + 32, 3, self.angle, 0,
                         True, False)
            self.angle += 36.533
            self.timer = 0

    def death(self,is_shoot):
        super().death(is_shoot)
        if is_shoot:
            ItemScore300(self.x + 32, self.y + 32)
        for i in range(1,50,1):
            BulletGravity(green1, self.x + 32, self.y + 32, random.randint(2,4), random.randint(180,359),35,0,15,True,
                          False)
        for i in range(1,5,1):
            BulletNormal(red1,self.x + 32, self.y + 32,i,
                         Enemy.player.get_player_angle(self.x+37,self.y+37),
                         0, False, False)
            BulletNormal(red1, self.x + 32, self.y + 32, i,
                         Enemy.player.get_player_angle(self.x + 37, self.y + 37) + math.radians(15),
                         0, False, False)
            BulletNormal(red1, self.x + 32, self.y + 32, i,
                         Enemy.player.get_player_angle(self.x + 37, self.y + 37) + math.radians(-15),
                         0, False, False)


class ScoreEnemy500(Enemy):
    def __init__(self, x, y):
        self.image = pygame.image.load(Menemy500).convert_alpha()
        super().__init__(x, y, 300, 0, 500)

    def update(self):
        super().update()
        if self.y >= 510:
            self.kill()

    def move(self):
        self.vy = 1

    def action(self):
        super().action()
        if self.timer == 30:
            for i in range(30,360,30):
                BulletTurbo3(red1,self.x + 32 ,self.y + 32,3,i+random.randint(1,5),0,0,2.5,60,60,False,False,True,False)
            self.timer = 0

    def death(self,is_shoot):
        super().death(is_shoot)
        if is_shoot:
            ItemScore500(self.x + 32, self.y + 32)
        for i in range(1, 10, 1):
            for j in range(0, 360, 12):
                BulletNormal(red1, self.x + 32, self.y + 32, i * 0.8, j + i * 0.5, i * 3, True, False)


class ScoreEnemy5000(Enemy):
    def __init__(self, x, y):
        self.image = pygame.image.load(Menemy5000).convert_alpha()
        super().__init__(x, y, 300, 0, 5000)

    def update(self):
        super().update()
        if self.y >= 510:
            self.kill()

    def move(self):
        self.vy = 1

    def action(self):
        super().action()

    def death(self,is_shoot):
        super().death(is_shoot)
        if is_shoot:
            ItemScore5000(self.x + 32, self.y + 32)
        for i in range(1, 6, 1):
            for j in range(0, 15, 1):
                BulletCurve(red1, self.x + 32, self.y + 32, i * 0.8, (j * 12) + j * 0.5, 5, 0, 10, True, False)
                BulletCurve(green1, self.x + 32, self.y + 32, i * 0.8, (j * 12) + j * 0.5, -5, 0, 10, True, False)


class ScoreEnemy10000(Enemy):
    def __init__(self, x, y):
        self.image = pygame.image.load(Menemy10000).convert_alpha()
        super().__init__(x, y, 500, 0, 10000)

    def update(self):
        super().update()
        if self.y >= 510:
            self.kill()

    def move(self):
        self.vy = 1

    def action(self):
        pass

    def death(self,is_shoot):
        super().death(is_shoot)
        if is_shoot:
            ItemScore5000(self.x + 32, self.y + 32)
