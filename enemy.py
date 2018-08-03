"""enemy system for pylaga

The All Important Enemy class, and its manager EnemyManager
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
from bullet import EnemyBullet


class EnemyManager(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.asdf = 0
        self.transition_speed = 5
        self.transition_time = 150 / self.transition_speed
        self.current_transition = 0

    def shoot(self, shotslist):
        self.asdf = random.randint(0, globalvars.enemy_bullet_odds)
        if self.asdf < len(self):
            self.sprites()[self.asdf].shoot(shotslist)

    def update(self):
        if self.current_transition < self.transition_time:
            for e in self:
                e.update(self.transition_speed)
            self.current_transition += 1
        else:
            for e in self:
                e.update(0)


# made into class as of "pylaga" fork
class Enemy(pygame.sprite.Sprite):
    enx = 0
    eny = 30
    # enspeed=globalvars.init_enemy_speed
    # envel=1
    # en_globalvars.xmax=globalvars.xmax
    #   # # come in very handy when there
    # is more than 1 enemy
    # en_globalvars.xmin=globalvars.xmin
    #   # # yeah what the first one said.^^
    # en_state=(-1)*(1)
    # image = globalvars.enemyship

    def __init__(self, parent):
        self.parent = parent
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.enspeed = globalvars.init_enemy_speed
        self.envel = 1
        self.en_xmax = globalvars.xmax
        self.en_xmin = globalvars.xmin
        self.en_state = (-1) * (1)  # TODO: why not -1??
        self.image = globalvars.enemyship
        self.rect = self.image.get_rect()

    # def get_pos(self):
        # return self.enx,self.eny

    def set_pos(self, tempx, tempy):
        self.rect.move_ip(tempx, tempy)

    def set_speed(self, speed):
        self.enspeed = speed

    def set_range(self, tempmin, tempmax):
        self.en_xmax = tempmax
        self.en_xmin = tempmin

    def get_range(self):
        return self.en_xmin, self.en_xmax

    def update(self, transition_speed):  # yay for update...
        # this is actually surgy's code but i adapted it to my own and
        # rewrote it so it uses < and > not == and !=
        if transition_speed > 0:
            self.rect.bottom += transition_speed
        elif self.envel <= 0:
            if self.rect.left < self.en_xmax:
                self.rect.right += self.enspeed
            elif self.rect.left >= self.en_xmax:
                self.envel = 1
        else:
            if self.rect.left > self.en_xmin:
                self.rect.right += ((-1) * self.enspeed)
            elif self.rect.left <= self.en_xmin:
                self.envel = 0
        self.next_state()

    # -1 is normal, 0 is exploding, up to 4 are the animations for it
    def set_state(self, varr):
        self.en_state = varr

    def next_state(self):
        if self.en_state >= 0 and self.en_state < 5:
            self.image = globalvars.explosions[self.en_state]
            self.en_state += 1
        elif self.en_state > 4:
            self.parent.remove(self)

    # return the state
    def get_state(self):
        return self.en_state

    def shoot(self, shotslist):
        tempb = EnemyBullet(shotslist)
        tempb.set_pos(self.rect.left + self.rect.width / 2,
                      self.rect.bottom)
        shotslist.add(tempb)
