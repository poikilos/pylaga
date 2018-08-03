"""enemy system for pylaga

The All Important Enemy class, and its manager Swarm
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


class Swarm(pygame.sprite.Group):
    def __init__(self, world_rect):
        self.world_rect = world_rect
        pygame.sprite.Group.__init__(self)
        self.asdf = 0
        self.transition_speed = 5
        self.transition_time = 150 / self.transition_speed
        self.current_transition = 0

    def shoot(self, image, bullet_spritegroup):
        self.asdf = random.randint(0, globalvars.enemy_bullet_odds)
        if self.asdf < len(self):
            self.sprites()[self.asdf].shoot(image, bullet_spritegroup)

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
    # self.world_rect.right
    #   # # come in very handy when there
    # is more than 1 enemy
    # swarm.world_rect.left
    #   # # yeah what the first one said.^^
    # en_state=(-1)*(1)

    def __init__(self, swarm, enemy_image, explosion_images):
        self.swarm = swarm
        self.world_rect = swarm.world_rect
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.enspeed = globalvars.init_enemy_speed
        self.envel = 1
        self.world_rect.right = swarm.world_rect.right
        self.world_rect.left = swarm.world_rect.left
        self.en_state = (-1) * (1)  # TODO: why not -1??
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.explosion_images = explosion_images

    # def get_dest_rect(self):
        # return self.enx,self.eny

    def set_pos(self, tempx, tempy):
        self.rect.move_ip(tempx, tempy)

    def set_speed(self, speed):
        self.enspeed = speed

    def set_range(self, tempmin, tempmax):
        self.world_rect.right = tempmax
        self.world_rect.left = tempmin

    def get_range(self):
        return self.world_rect.left, self.world_rect.right

    def update(self, transition_speed):  # yay for update...
        # this is actually surgy's code but i adapted it to my own and
        # rewrote it so it uses < and > not == and !=
        if transition_speed > 0:
            self.rect.bottom += transition_speed
        elif self.envel <= 0:
            if self.rect.left < self.world_rect.right:
                self.rect.right += self.enspeed
            elif self.rect.left >= self.world_rect.right:
                self.envel = 1
        else:
            if self.rect.left > self.world_rect.left:
                self.rect.right += ((-1) * self.enspeed)
            elif self.rect.left <= self.world_rect.left:
                self.envel = 0
        self.next_state()

    # -1 is normal, 0 is exploding, up to 4 are the animations for it
    def set_state(self, varr):
        self.en_state = varr

    def next_state(self):
        if self.en_state >= 0 and self.en_state < 5:
            self.image = self.explosion_images[self.en_state]
            self.en_state += 1
        elif self.en_state > 4:
            self.swarm.remove(self)

    # return the state
    def get_state(self):
        return self.en_state

    def shoot(self, image, spritegroup):
        tempb = EnemyBullet(image, spritegroup, self.world_rect)
        tempb.set_pos(self.rect.left + self.rect.width / 2,
                      self.rect.bottom)
        spritegroup.add(tempb)
