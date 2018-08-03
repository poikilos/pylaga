"""global variables for pylaga

The Background Manager, which manages stars
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


# makes a globalvars.background that moves and stuff
class BackgroundManager(pygame.sprite.Sprite):

    star_rects = []
    prev_star_rects = []

    def __init__(self, bg_rect):
        self.bg_rect = bg_rect
        for x in range(globalvars.init_stars):
            self.add_star()

    def update(self):
        # self.prev_star_rects = [pygame.Rect(st) for st in self.star_rects \
        # if st.top <= self.bg_rect.bottom]
        # ugh thanks guy online, this saved me

        for counter, star in enumerate(self.star_rects):
            if star.top > self.bg_rect.bottom:
                del self.star_rects[counter]
                del self.prev_star_rects[counter]
                self.add_star()
            else:
                self.prev_star_rects[counter].topleft = star.topleft
                star.top += star.speed
                # print(str(star) + str(self.prev_star_rects[counter]))

    def draw(self, screen):
        # TODO: eliminate this
        for star in self.star_rects:
            screen.fill(globalvars.star_color, star)
        return self.star_rects

    # def clear(self, screen):
        # for star in self.prev_star_rects:
            # screen.fill(globalvars.bg_color, star)
        # return self.prev_star_rects

    def add_star(self):
        size = random.randint(3, 6)
        x = random.randint(0, self.bg_rect.right)
        rect = Star(x, 0, size, size)
        rect.set_speed(random.randint(2, globalvars.BG_Speed))
        self.star_rects.append(rect)
        self.prev_star_rects.append(pygame.Rect(rect))


class Star(pygame.Rect):

    def set_speed(self, tspeed):
        self.speed = tspeed

    def get_speed(self):
        return self.speed

