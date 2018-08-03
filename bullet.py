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
import globalvars


# A bullet class, simple, but it does keep track of its location and
# saves the main thread some work
class Bullet(pygame.sprite.Sprite):
    def __init__(self, parentlist):
        self.parentlist = parentlist
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = globalvars.shot  # sets the image
        self.rect = self.image.get_rect()  # sets rect associated with image
        self.bspeed = globalvars.BULLET_SPEED  # sets the speed
        self.health = 1

    def set_pos(self, tempx, tempy):
        self.rect.move_ip(tempx, tempy)

    def set_hit(self):
        self.health -= 1

    def set_speed(self, speed):
        self.bspeed = speed

    def update(self):
        self.rect.move_ip(0, -1*(self.bspeed))  # remember, STARTS at highest Y
        if self.rect.bottom <= 0 or self.health <= 0:
            self.parentlist.remove(self)


# Extension of bullet class to draw bullets
# It needs to know what list its been added to
class EnemyBullet(Bullet):

    def __init__(self, parentlist):
        self.parentlist = parentlist
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = globalvars.eshot  # sets the image
        self.rect = self.image.get_rect()  # sets rect associated with image
        self.bspeed = globalvars.BULLET_SPEED  # sets the speed
        self.health = 1

    def update(self):
        self.rect.move_ip(0, (self.bspeed))  # remember, STARTS at highest Y
        if self.rect.bottom > globalvars.WIN_RESY:
            self.parentlist.remove(self)
