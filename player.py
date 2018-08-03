#!/usr/bin/env python
"""PlayerUnit for pylaga

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
from globalvars import explosion_speed
from bullet import Bullet


################
# origional program had a few boring player lines, so i made it an
# object, cuz objects are cool
class PlayerUnit(pygame.sprite.Sprite):

    def __init__(self, image_list):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.images = image_list
        self.image = image_list[0]
        self.rect = self.image.get_rect()
        self.state = 0
        self.speed = 10

    def get_dest_rect(self):
        return self.rect

    def set_xy(self, x, y):
        self.rect.topleft = (x, y)

    def get_pos(self):
        return self.rect.topleft

    def move_one(self, direction, world_rect):
        if direction > 0:
            self.rect.move_ip(self.speed, 0)
            if not self.in_range(world_rect):
                # if it goes out of the range, move it back
                self.rect.move_ip((-1)*self.speed, 0)
        elif direction == 0:
            print("WARNING in move_one: nothing done since value is " +
                  str(direction))
        else:
            self.rect.move_ip((-1)*self.speed, 0)
            if not self.in_range(world_rect):
                self.rect.move_ip(self.speed, 0)

    def in_range(self, range_rect):
        if range_rect.contains(self.rect):
            return True
        return False

    def set_pos(self, x, y):
        self.rect.move_ip(x, y)
        print("set_pos: player rect: " + str(self.rect))

    def set_hit(self):
        self.state = 1

    def shoot(self, image, spritegroup, locx, locy):
        self.boom = Bullet(image, spritegroup)
        self.boom.set_pos(locx, locy)
        # self.boom.set_speed(globalvars.BUL)
        spritegroup.add(self.boom)

    def update(self):  # yay for update...
        if self.state > 0:
            self.image = self.images[int(self.state/explosion_speed)]
            self.state += 1
            if self.state >= len(self.images) * explosion_speed:
                self.state = 0
                self.image = self.images[0]
