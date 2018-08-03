#!/usr/bin/env python
"""Player for pylaga

The player class
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
from globalvars import playership, explosion_speed, gamewindow
from bullet import Bullet


################
# origional program had a few boring player lines, so i made it an
# object, cuz objects are cool
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = playership[0]
        self.rect = self.image.get_rect()
        self.state = 0
        self.speed = 10

    def get_pos(self):
        return self.rect

    def move(self, x, y):
        self.rect.topleft = (x, y)

    def move_one(self, direction):
        if direction == 1:
            self.rect.move_ip(self.speed, 0)
            if not self.in_range(self.rect):
                    # if it goes out of the range, move it back
                self.rect.move_ip((-1)*self.speed, 0)
        elif direction == 0:
            self.rect.move_ip((-1)*self.speed, 0)
            if not self.in_range(self.rect):
                self.rect.move_ip(self.speed, 0)

    def in_range(self, rect):
        if gamewindow.contains(rect):
            return True
        return False

    def set_pos(self, tempx, tempy):
        self.rect.move_ip(tempx, tempy)

    def set_hit(self):
        self.state = 1

    def shoot(self, shotslist, locx, locy):
        self.boom = Bullet(shotslist)
        self.boom.set_pos(locx, locy)
        # self.boom.set_speed(globalvars.BUL)
        shotslist.add(self.boom)

    def update(self):  # yay for update...
        if self.state > 0:
            self.image = playership[int(self.state/explosion_speed)]
            self.state += 1
            if self.state >= len(playership) * explosion_speed:
                self.state = 0
                self.image = playership[0]
