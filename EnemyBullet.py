# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import math

class EnemyBullet(pygame.sprite.Sprite):
    containers = None
    player = None
    enemy_bullet_group = None

    def __init__(self, filename, x, y, speed, angle, delay, enable_radian=False, bomb_resistant=False):
        pygame.sprite.Sprite.__init__(self, EnemyBullet.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x - (self.width / 2)
        self.y = y - (self.height / 2)
        self.rect = Rect(x, y, self.width, self.height)
        self.rect.center = (x / self.width, y / self.height)
        enable_radian = bool(enable_radian)
        if enable_radian:
            self.angle = math.radians(angle)
        elif not enable_radian:
            self.angle = angle
        if self.angle >= 360:
            self.angle -= 360
        self.speed = speed
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        self.radius = (self.width / 6) + (self.height / 6)
        self.delay = delay
        self.bomb_resistant = bool(bomb_resistant)

    def update(self):
        if self.delay == 0:
            self.x += self.vx
            self.y += self.vy
        else:
            self.delay -= 1
        self.rect.x = self.x
        self.rect.y = self.y

        if (EnemyBullet.player.bomb_flag or EnemyBullet.player.BulletAnti) and not self.bomb_resistant:
            self.kill()

        self.rect_kill()

    def rect_kill(self):
        if self.rect.x <= -40:
            self.kill()
        if self.rect.y <= -40:
            self.kill()
        if self.rect.x >= 700:
            self.kill()
        if self.rect.y >= 540:
            self.kill()

    @classmethod
    def sprite_group_registry(cls, *groups):
        cls.containers = groups

    @classmethod
    def player_registry(cls,player):
        cls.player = player

    @classmethod
    def group_registry(cls,group):
        cls.enemy_bullet_group = group


class BulletNormal(EnemyBullet):
    def __init__(self, filename, x, y, speed, angle, delay, enable_radian=False, bomb_resistant=False):
        super().__init__(filename, x, y, speed, angle, delay, enable_radian, bomb_resistant)


# カーブ弾　ギミック:有効時間内に角度が徐々に曲がる
class BulletCurve(EnemyBullet):
    def __init__(self, filename, x, y, speed, angle, vector_angle, delay, timer, enable_radian=False,
                 bomb_resistant=False):
        super().__init__(filename, x, y, speed, angle, delay, enable_radian, bomb_resistant)
        if enable_radian:
            self.vector_angle = math.radians(vector_angle)
        elif not enable_radian:
            self.vector_angle = vector_angle
        self.timer = timer

    def update(self):
        self.timer -= 1

        if self.timer >= 0:
            self.angle += self.vector_angle
        if self.timer <= 0:
            self.timer = 0
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        super().update()


# カーブ弾2　ギミック:指定された時間に経つと、角度を変更する　また回数を指定するとその回数分繰り返す
class BulletCurve2(EnemyBullet):
    def __init__(self, filename, x, y, speed, angle, vector_angle, delay, time, count=1, enable_radian=False,
                 bomb_resistant=False):
        super().__init__(self, filename, x, y, speed, angle, delay, enable_radian)
        if enable_radian:
            self.vector_angle = math.radians(vector_angle)
        elif not enable_radian:
            self.vector_angle = vector_angle
        self.reset_time = time
        self.time = time
        self.count = count

    def update(self):
        if self.angle >= 360:
            self.angle -= 360
        if self.count > 0:
            self.time -= 1
            if self.time <= 0:
                self.angle += self.vector_angle
                self.time = self.reset_time
                self.count -= 1
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        super().update()


# 加速弾    ギミック:徐々に加速する
class BulletTurbo(EnemyBullet):
    def __init__(self, filename, x, y, speed, angle, delay, acceleration, enable_radian=False, bomb_resistant=False):
        super().__init__(filename, x, y, speed, angle, delay, enable_radian, bomb_resistant)
        self.acceleration = acceleration

    def update(self):
        self.speed += self.acceleration / 10
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        super().update()



# 加速弾2       ギミック:時間指定で加速する
class BulletTurbo2(EnemyBullet):
    def __init__(self, filename, x, y, speed, angle, delay, time, acceleration, enable_radian=False,
                 bomb_resistant=False):
        super().__init__(filename, x, y, speed, angle, delay, enable_radian, bomb_resistant)
        self.acceleration = acceleration
        self.time = time

    def update(self):
        self.time -= 1
        if self.time <= 0:
            self.speed += self.acceleration
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        super().update()



# 加速弾3   ギミック:指定時間で、一旦停止し、指定したスピードで再び動く  オプション:角度変化,角度変化の仕方(0なら加算,1なら代入),加速の仕方(0なら徐々に,1なら急加速)
class BulletTurbo3(EnemyBullet):
    def __init__(self, filename, x, y, speed, angle, vector_angle, delay, acceleration, start_time, stop_time,
                 angle_instant=False, speed_instant=False,
                 enable_radian=False, bomb_resistant=False):
        super().__init__(filename, x, y, speed, angle, delay, enable_radian, bomb_resistant)
        if enable_radian:
            self.vector_angle = math.radians(vector_angle)
        elif not enable_radian:
            self.vector_angle = vector_angle
        if self.angle >= 360:
            self.angle -= 360
        self.stop_time = stop_time
        self.start_time = start_time
        self.acceleration = acceleration
        self.angle_instant = angle_instant
        self.started = False
        self.speed_instant = speed_instant

    def update(self):
        self.stop_time -= 1
        if self.stop_time <= 0:
            self.stop_time = 0
            self.speed -= self.speed / 10
            if self.speed < 0:
                self.speed = 0
            self.start_time -= 1
            if self.start_time <= 0:
                self.bullet_start()
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        super().update()

    def bullet_start(self):
        if self.vector_angle >= 1:
            if not (self.angle_instant and self.started):
                self.angle += self.vector_angle
                self.started = True
            elif self.angle_instant and not self.started:
                self.angle = self.vector_angle
                self.started = True
        if not self.speed_instant:
            self.speed += self.acceleration / 10
            if self.speed >= self.acceleration + self.speed:
                self.speed = self.acceleration
        elif self.speed_instant:
            self.speed = self.acceleration


# 加速弾4   ギミック:時間指定で徐々に減速し、急加速する
class BulletTurbo4(EnemyBullet):
    containers = None

    def __init__(self, filename, x, y, before_speed, after_speed, angle, delay, time, enable_radian=False,
                 bomb_resistant=False):
        super().__init__(filename, x, y, before_speed, angle, delay, enable_radian, bomb_resistant)
        self.after_speed = after_speed
        self.time = time
        self.timelimit = time
        self.stop = False

    def update(self):
        if not self.stop:
            self.time -= 1
        else:
            self.time += 1

        if self.time <= 0:
            self.stop = True
            self.speed = self.speed / 10
        elif self.time >= self.timelimit:
            self.speed = self.after_speed
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        super().update()



# バウンド弾      ギミック:壁に衝突すると、跳ね返る
class BulletBound(EnemyBullet):
    containers = None

    def __init__(self, filename, x, y, speed, angle, delay, count=1, enable_radian=False, bomb_resistant=False):
        super().__init__(filename, x, y, speed, angle, delay, enable_radian, bomb_resistant)
        self.count = count
        self.delay = 0
        self.bflag = 0

    def update(self):
        self.delay -= 1
        if self.delay <= 0:
            self.bflag = 0
            self.delay = 0

        if self.bflag == 0 and (self.count > 0 or self.count == -1):
            if self.rect.x <= -20:
                self.angle += math.radians(180)
                self.bflag = 1
                self.delay = 60
                self.count -= 1
            if self.rect.y <= -20:
                self.angle += math.radians(180)
                self.bflag = 1
                self.delay = 60
                self.count -= 1
            if self.rect.x >= 680:
                self.angle += math.radians(180)
                self.bflag = 1
                self.delay = 60
                self.count -= 1
            if self.rect.y >= 240:
                self.angle += math.radians(180)
                self.bflag = 1
                self.delay = 60
                self.count -= 1
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        super().update()



# 分裂弾    ギミック:指定時間経過で、別の弾を打つ
# 課題     どうやって、別クラスの弾を生成させるか
class BulletVariance(EnemyBullet):
    def __init__(self, filename, x, y, speed, angle, fire_time, count, filename2, vector_angle, delay,
                 enable_radian=False,
                 vector_enable_radian=False, bomb_resistant=False, is_vanish=True):
        super().__init__(filename, x, y, speed, angle, delay, enable_radian, bomb_resistant)
        self.filename2 = filename2
        self.count = count
        self.vector_angle = vector_angle
        self.vector_enable_radian = vector_enable_radian
        self.time = fire_time
        self.reset_time = fire_time
        self.BombResist = bomb_resistant
        self.is_vanish = is_vanish

    def update(self):
        self.time -= 1
        if self.time <= 0:
            for i in range(0, self.count, 1):
                BulletNormal(self.filename2, self.x + (self.width / 2), self.y + (self.height / 2), self.speed,
                             self.vector_angle * i, 0,
                             self.vector_enable_radian)
            if self.is_vanish:
                self.kill()
            else:
                self.time = self.reset_time
        super().update()



# ホーミング弾　ギミック：自機の方に向く
class BulletHoming(EnemyBullet):

    def __init__(self, filename, x, y, speed, angle, delay=120, timer=60, enable_radian=False, bomb_resistant=False):
        super().__init__(filename, x, y, speed, angle, enable_radian, bomb_resistant)
        self.delay = delay
        self.timer = timer
        self.reset_time = timer

    def update(self):
        if self.delay <= 0:
            self.timer -= 1
        if self.timer <= 0:
            self.timer = self.reset_time
            self.angle = EnemyBullet.player.getPlayerAngle(self.x, self.y)
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        super().update()



# 重力弾　　ギミック：指定時間経過で徐々に下に傾く

class BulletGravity(EnemyBullet):
    containers = None

    def __init__(self, filename, x, y, speed, angle, vector_angle, delay, timer=60, enable_radian=False,
                 bomb_resistant=False):
        super().__init__(filename, x, y, speed, angle, delay, enable_radian, bomb_resistant)
        self.timer = timer
        self.vector_angle = vector_angle

    def update(self):
        self.timer -= 1
        if self.angle >= math.radians(360):
            self.angle -= math.radians(360)
        if self.timer <= 0:
            if math.radians(90) < self.angle and self.angle < math.radians(270):
                self.angle -= math.radians(self.vector_angle) / 10
            if math.radians(270) < self.angle and self.angle < math.radians(361):
                self.angle += math.radians(self.vector_angle) / 10
            if math.radians(0) <= self.angle  and self.angle < math.radians(90):
                self.angle += math.radians(self.vector_angle) / 10

        if self.angle >= 360:
            self.angle -= 360
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        super().update()


