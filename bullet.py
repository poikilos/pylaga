"""bullets for pylaga

A simple bullet class, and a subclass, EnemyBullet
"""

__author__ = ("2007-02-20 Derek Mcdonald (original),"
              " 2007-04-1 RJ Marsan,"
              " 2018 poikilos (Jake Gustafson)")
__version__ = '0.2.1'
__all__ = []

import pygame
import os
import sys
import math
import random


# A bullet class, simple, but it does keep track of its location and
# saves the main thread some work
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, spritegroup, bullet_speed=10, bullet_width=10):
        self.spritegroup = spritegroup
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.bspeed = bullet_speed
        self.bwidth = bullet_width
        self.health = 1

    def move_by(self, tempx, tempy):
        self.rect.move_ip(tempx, tempy)

    def set_hit(self):
        self.health -= 1

    def set_speed(self, speed):
        self.bspeed = speed

    def update(self):
        self.rect.move_ip(0, -1*(self.bspeed))  # START at highest Y
        if self.rect.bottom <= 0 or self.health <= 0:
            self.spritegroup.remove(self)


# Extension of bullet class to draw bullets
# It needs to know what list its been added to
class EnemyBullet(Bullet):

    def __init__(self, image, spritegroup, world_rect,
                 speed=10, width=10):
        self.world_rect = world_rect
        self.spritegroup = spritegroup
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.bspeed = speed
        self.health = 1

    def update(self):
        self.rect.move_ip(0, (self.bspeed))  # START at highest Y
        if self.rect.bottom > self.world_rect.bottom:
            self.spritegroup.remove(self)
        # TODO: delete if off screen in other directions
