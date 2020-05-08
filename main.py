# -*- coding: utf-8 -*-
from Enemy import *
from Items import *
from common import ScoreData
from imglibrary import *
from SElibrary import *

import pygame
from pygame.locals import *
import math
import sys


# ゲーム本体のクラス
class MainGame:
    # クラス変数
    screen = None  # 画面を表示するため
    life = 3
    player = None  # プレイヤーインスタンス
    boss = None  # ボスインスタンス
    sprite_all = None  # スプライト全体グループ
    ItemGroup = None  # スプライトアイテムグループ
    EnemyBulletGroup = None  # スプライト敵弾グループ
    EnemyGroup = None  # スプライト敵グループ
    PlayerBulletGroup = None  # スプライトプレイヤーの弾グループ

    '''
    # サウンド
    player_bomb_sound = None  # プレイヤーがボムを使用したときの効果音
    shoot_sound = None  # プレイヤーが敵を倒したときの効果音
    player_hit_sound = None  # プレイヤーが敵、敵弾とぶつかったときの効果音
    item_get_sound = None  # プレイヤーがアイテムを取得したときの効果音
    '''

    # UI関係
    UI_Score = None
    UI_Bomb = None
    UI_Life = None
    ClearMes1 = None
    ClearMes2 = None
    GameOver1 = None
    GameOver2 = None

    # クラス定数
    WIRE_FRAME_COLOR = (0, 255, 0)  # 背景に用いるワイヤーフレームの色
    NORMAL_COLOR = (255, 255, 255)
    WARNING_COLOR = (255, 0, 0)  # 警告色　赤色
    START_PLAYER_X = 320  # プレイヤーの開始、復活位置X
    START_PLAYER_Y = 370  # プレイヤーの開始、復活位置Y

    def __init__(self):
        # ゲームの準備
        pygame.mixer.quit()
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()

        # 　インスタンス変数
        self.by = [i * 64 for i in range(-1, 10, 1)]  # ワイヤーフレーム背景用の配列　[-64,0,64...]
        self.back_speed = 0  # ワイヤーフレームの背景動作スピード
        self.scrolled = 0  # 進行度
        self.BossFlag = False  # ボス出現フラグ
        self.clear = False  # ゲームクリアフラグ
        self.wait = 600

        # 初期化
        MainGame.screen = pygame.display.set_mode([640, 480], FULLSCREEN)  # ゲーム画面設定、フルスクリーンで起動
        pygame.display.set_caption("弾幕もどき")  # ウィンドウのタイトル
        self.system_font = pygame.font.SysFont(None, 40)  # ゲーム画面に用いるフォント
        clock = pygame.time.Clock()  # ゲーム内の同期クロック

        #   効果音と変数の対応付け
        '''
        MainGame.player_bomb_sound = pygame.mixer.Sound(PBomb)
        MainGame.shoot_sound = pygame.mixer.Sound(shoot)
        MainGame.player_hit_sound = pygame.mixer.Sound(Player_Hit)
        MainGame.item_get_sound = pygame.mixer.Sound(item_get)
        '''

        # 衝突判定グループ
        MainGame.sprite_all = pygame.sprite.RenderUpdates()
        MainGame.ItemGroup = pygame.sprite.Group()
        MainGame.EnemyBulletGroup = pygame.sprite.Group()
        MainGame.EnemyGroup = pygame.sprite.Group()
        MainGame.PlayerBulletGroup = pygame.sprite.Group()

        # 　 衝突グループ、登録
        BulletPlayer.registry(MainGame.sprite_all, MainGame.PlayerBulletGroup)
        Enemy.registry(MainGame.sprite_all, MainGame.EnemyGroup, MainGame.EnemyBulletGroup)
        EnemyBullet.sprite_group_registry(MainGame.sprite_all, MainGame.EnemyBulletGroup)
        Player.containers = MainGame.sprite_all
        Item.registry(MainGame.sprite_all, MainGame.ItemGroup)
        MainGame.player = Player(PLAYER, MainGame.START_PLAYER_X, MainGame.START_PLAYER_Y)

        #   プレイヤーの参照渡し
        EnemyBullet.player_registry(MainGame.player)

        Item.player_registry(MainGame.player)
        Item.sprite_registry(MainGame.ItemGroup)
        #Item.get_sound_load(MainGame.item_get_sound)

        Enemy.player_registry(MainGame.player)
        Enemy.player_bullet_group_registry(MainGame.PlayerBulletGroup)
        #Enemy.shoot_sound_registry(MainGame.shoot_sound)

        # ゲームループ
        while True:
            pygame.display.update()  # 表示更新メソッド
            clock.tick(60)  # 同期時間 60=1秒
            self.update()  # 更新メソッド
            self.draw(MainGame.screen)  # 描画メソッド

    def update(self):
        self.scrolled += 1
        # 更新　エスケープキーを押すと終了処理をする
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # ステージ構成
        # if文で強引にステージを成立させている
        if self.scrolled == 240:
            Enemy1(180, -50, 100, 0, 4)
            Enemy1(450, -50, 100, 0, 4)
            ScoreEnemy100(30, -50)
            ScoreEnemy100(500, -50)
        if self.scrolled == 780:
            ScoreEnemy500(320,-50)
        if self.scrolled == 1800:
            MainGame.boss = Stage1MBoss(250, -80)
            self.scrolled += 1
        if self.scrolled == 2000:
            Enemy1(90, -50, 100, 4, 4)
            Enemy1(120, -50, 100, 2, 4)
            Enemy2(200, -50, 100, 1, 4)
            Enemy2(240, -50, 100, 2, 4)
        if self.scrolled == 2100:
            Enemy2(90, -50, 100, 2, 4)
            Enemy2(120, -50, 100, 1, 4)
            Enemy2(200, -50, 100, 1, 4)
            Enemy2(240, -50, 100, 2, 4)
            ScoreEnemy5000(420, -50)
            ScoreEnemy100(500, -50)
        if self.scrolled == 2200:
            Enemy1(90, -50, 100, 2, 4)
            Enemy1(120, -50, 100, 1, 4)
            Enemy1(200, -50, 100, 1, 4)
            Enemy1(240, -50, 100, 2, 4)
        if self.scrolled == 2300:
            Enemy2(90, -50, 100, 1, 4)
            Enemy1(120, -50, 100, 3, 4)
            Enemy1(200, -50, 100, 3, 4)
            Enemy2(240, -50, 100, 1, 4)
        if self.scrolled == 3000:
            MainGame.boss = Stage1boss(250, -80)
            self.scrolled += 1
        if self.scrolled == 3400:
            self.clear = True

        MainGame.sprite_all.update()

        if MainGame.life == 0:
            self.wait -= 1
            pressedkey = pygame.key.get_pressed()
            if pressedkey[K_z] and self.wait <= 0:
                self.wait = 600
                self.scrolled = 0
                if MainGame.boss:
                    MainGame.boss.kill()
                    MainGame.boss = None
                for x in MainGame.EnemyGroup:
                    x.kill()
                MainGame.ItemGroup.empty()
                MainGame.EnemyBulletGroup.empty()
                ScoreData.score = 0
                MainGame.life = 3
                MainGame.player.__init__(PLAYER,MainGame.START_PLAYER_X,MainGame.START_PLAYER_Y)

        pygame.display.flip()
        pygame.display.update()

    def draw(self, screen):

        # 　UI関係
        #   残機が1個だけなら、赤色にそれ以外は白色に表示する
        if MainGame.life == 1:
            ui_color = MainGame.WARNING_COLOR
        else:
            ui_color = MainGame.NORMAL_COLOR

        #  表示する文字UI
        MainGame.UI_Score = self.system_font.render("Score:{}".format(ScoreData.score), True, ui_color)
        MainGame.UI_Bomb = self.system_font.render("Bomb:{}".format(MainGame.player.has_bomb), True, ui_color)
        MainGame.UI_Life = self.system_font.render("Life:{}".format(MainGame.life), True, ui_color)
        MainGame.ClearMes1 = self.system_font.render("Game Clear!", True, (0, 255, 255))
        MainGame.ClearMes2 = self.system_font.render("Press Esc key is Game End.", True, (0, 255, 255))
        MainGame.GameOver1 = self.system_font.render("GAME OVER", True, (0, 255, 255))
        MainGame.GameOver2 = self.system_font.render("Press Enter z is Retry.Press Esc key is Game End.", True, (0, 255, 255))

        # 背景の動作
        if self.scrolled == 0:
            self.back_speed = 0
        if self.scrolled == 240:
            self.back_speed = 1
        if self.BossFlag and (1800 <= self.scrolled and self.scrolled >= 1803):
            self.back_speed = 0
        if self.scrolled == 2000:
            self.back_speed = 1
        if self.scrolled == 2400:
            self.back_speed = 3
        if self.scrolled == 2600:
            self.back_speed = 5
        if self.scrolled == 3000:
            self.back_speed = 9
        if self.BossFlag and (3200 <= self.scrolled and self.scrolled >= 3206):
            self.back_speed = 9

        if MainGame.boss is not None:
            if 1 <= MainGame.boss.hp:
                self.scrolled -= 1
                ui_boss_hp = self.system_font.render(
                    "Target:{}%".format(math.floor((MainGame.boss.hp / MainGame.boss.max_hp) * 100)), True, ui_color)
            elif MainGame.boss.hp <= 0:
                MainGame.boss = None

        # 描画 ワイヤーフレーム背景
        screen.fill((0, 0, 0))
        for j in range(0, 11, 1):
            pygame.draw.line(MainGame.screen, MainGame.WIRE_FRAME_COLOR, (0, self.by[j]), (640, self.by[j]), 1)
            self.by[j] += self.back_speed
            if self.by[j] > 640:
                self.by[j] = -64
            if self.by[j] < -65:
                self.by[j] = 640
        for i in range(0, 11, 1):
            pygame.draw.line(MainGame.screen, MainGame.WIRE_FRAME_COLOR, (i * 63, 0), (i * 63, 480), 1)
        MainGame.sprite_all.draw(MainGame.screen)

        if self.clear:
            screen.blit(MainGame.ClearMes1, (100, 240))
            screen.blit(MainGame.ClearMes2, (100, 270))
            screen.blit(MainGame.UI_Score, (100, 300))
        elif MainGame.life == 0:
            screen.blit(MainGame.GameOver1, (100, 240))
            if self.wait <= 0:
                screen.blit(MainGame.GameOver2, (100, 270))
            screen.blit(MainGame.UI_Score, (100, 300))
        else:
            screen.blit(MainGame.UI_Score, (0, 0))
            screen.blit(MainGame.UI_Bomb, (0, 25))
            screen.blit(MainGame.UI_Life, (0, 50))
        if MainGame.boss is not None:
            if MainGame.boss.hp >= 1:
                screen.blit(ui_boss_hp, (475, 0))

    @classmethod
    def player_hit(cls):
        cls.life -= 1


class ItemBomb(pygame.sprite.Sprite):
    containers = None

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, ItemBomb.containers)
        self.image = pygame.image.load(BombG).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x, y, width, height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = 0
        self.vy = 1.25

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y

        # RectKill(self)

    def draw(self, screen):
        screen.blit(self.image.self.rect)


class Item1UP(pygame.sprite.Sprite):
    containers = None

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, Item1UP.containers)
        self.image = pygame.image.load(OneUPG).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x, y, width, height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = 0
        self.vy = 1.25

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y

        # RectKill(self)

    def draw(self, screen):
        screen.blit(self.image.self.rect)


# ------------------------------------------------------

# =プレイヤー専用の弾
class BulletPlayer(pygame.sprite.Sprite):
    containers = None

    def __init__(self, filename, x, y, speed, angle):
        pygame.sprite.Sprite.__init__(self, BulletPlayer.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        x -= width / 2
        y -= height / 2
        self.x = x
        self.y = y
        self.rect = Rect(x, y, width, height)
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

        Ecollide = pygame.sprite.spritecollide(self, MainGame.EnemyGroup, False, pygame.sprite.collide_circle)
        if Ecollide:
            self.Timer -= 2.5
        if self.Timer <= 0:
            self.kill()
        self.rect_kill()

    def draw(self, screen):
        screen.blit(self.image.self.rect)

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
    def registry(cls, *groups):
        cls.containers = groups


# PlayerClass

class Player(pygame.sprite.Sprite):
    containers = None

    def __init__(self, filename, x, y, Bomb=3):
        pygame.sprite.Sprite.__init__(self, Player.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x, y, width, height)
        self.rect.center = (x / width, y / height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = 0
        self.vy = 0
        self.speed = 3
        self.reload = 0
        self.radius = 3
        self.eraser = 0
        self.death_flag = False
        self.has_bomb = Bomb
        self.bomb_flag = False
        self.bomb_time = 180
        self.radius = 1
        self.invisibility = 1
        self.invisible_time = 60
        self.BulletAnti = 1

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx = 0
        self.vy = 0
        self.rect.x = self.x
        self.rect.y = self.y
        self.reload -= 1

        if self.invisible_time > 0:
            self.invisibility = True
            self.BulletAnti = True
            self.invisible_time -= 1

        if self.invisible_time == 0:
            self.invisibility = False
            self.BulletAnti = False

        if self.bomb_flag == 1:
            self.bomb_time -= 1
            self.invisibility = 1
        if self.bomb_time <= 0:
            self.bomb_flag = 0
            self.bomb_time = 180
            self.invisibility = 0

        if MainGame.life == 0:
            return
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
                BulletPlayer(PlayerB, self.rect.x + 6, self.rect.y + 6, 11, 270)
                BulletPlayer(PlayerB, self.rect.x + 16, self.rect.y + 6, 11, 270)
                self.reload = 4
        if presskeys[K_x] and self.bomb_flag == 0 and self.has_bomb >= 1:
            if self.bomb_time == 180:
                pass
                #MainGame.player_bomb_sound.play()
            self.bomb_flag = 1
            self.has_bomb -= 1
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
        collide = pygame.sprite.spritecollide(MainGame.player, MainGame.EnemyBulletGroup, False,
                                              pygame.sprite.collide_circle)
        if collide and self.invisibility == 0:
            # MainGame.player_hit_sound.play()
            self.x = MainGame.START_PLAYER_X
            self.y = MainGame.START_PLAYER_Y
            self.set_invisibility(60)
            MainGame.player_hit()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def set_invisibility(self, sec):
        self.invisible_time = sec

    def get_xy(self):
        return self.x, self.y

    def get_player_angle(self, x, y):
        return math.atan2(self.rect.centery - y, self.rect.centerx - x)

    @classmethod
    def get_player_xy(cls):
        return cls.getXY()


if __name__ == "__main__":
    MainGame()
