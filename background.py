"""global variables for pylaga

The Background Manager and its subclass, star
Also the global object bgstars
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

    stars = []
    last_stars = []

    def __init__(self):
        for x in range(globalvars.init_stars):
            self.add_star()

    def update(self):
        # self.last_stars = [pygame.Rect(st) for st in self.stars \
        # if st.top <= globalvars.WIN_RESY]
        # ugh thanks guy online, this saved me

        for counter, star in enumerate(self.stars):
            if star.top > globalvars.WIN_RESY:
                del self.stars[counter]
                del self.last_stars[counter]
                self.add_star()
            else:
                self.last_stars[counter].topleft = star.topleft
                star.top += star.speed
                # print(str(star) + str(self.last_stars[counter]))

    def draw(self):
        for star in self.stars:
            globalvars.surface.fill(globalvars.star_color, star)
        return self.stars

    def clear(self):
        for star in self.last_stars:
            globalvars.surface.fill(globalvars.bgcolor, star)
        return self.last_stars

    def add_star(self):
        size = random.randint(3, 6)
        x = random.randint(0, globalvars.WIN_RESX)
        rect = star(x, 0, size, size)
        rect.set_speed(random.randint(2, globalvars.BG_Speed))
        self.stars.append(rect)
        self.last_stars.append(pygame.Rect(rect))


class star(pygame.Rect):

    def set_speed(self, tspeed):
        self.speed = tspeed

    def get_speed(self):
        return self.speed

global bgstars
bgstars = BackgroundManager()
