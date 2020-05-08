import pygame
from pygame.locals import *
from imglibrary import *
from common import ScoreData

class Item(pygame.sprite.Sprite):
    containers = None
    _item_graphic = {100: Score100, 300: Score300, 500: Score500, 900: Score900, 2000: Score2000, 5000: Score5000,
                     10000: Score10000}
    player = None
    item_group = None
    get_sound = None

    def __init__(self, x, y, score=0):
        pygame.sprite.Sprite.__init__(self, Item.containers)
        self.image = pygame.image.load(Item._item_graphic[score]).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.x = x
        self.y = y
        self.rect = Rect(x, y, width, height)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vx = 0
        self.vy = 1.25
        self.score = score

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y
        collide = pygame.sprite.spritecollide(Item.player, Item.item_group, True, pygame.sprite.collide_circle)
        if collide:
            self.trigger()
        self.rect_kill()

    def draw(self, screen):
        screen.blit(self.image.self.rect)

    def trigger(self):
        ScoreData.add_score(self.score)
        #Item.get_sound.play()
        self.kill()

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

    @classmethod
    def player_registry(cls,player):
        cls.player = player

    @classmethod
    def sprite_registry(cls,group):
        cls.item_group = group

    @classmethod
    def get_sound_load(cls,sound):
        cls.get_sound = sound


class ItemScore100(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 100)


class ItemScore300(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 300)


class ItemScore500(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 500)


class ItemScore900(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 900)


class ItemScore2000(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 2000)


class ItemScore5000(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 5000)


class ItemScore10000(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 10000)
