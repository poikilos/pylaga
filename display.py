"""hud for pylaga

Blah. the display. points, health and hud
This whole file needs to be cleaned up to adhere to the
globalvars more, I'm lazy.
Scratch that. we need to get rid of globalvars altogether.
DEATH TO GLOBAL VARS!
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
# TODO: Eliminate global vars


###################
# TODO: i needed to make this an object because i couldnt figure out how
# to make it globally available but also writable
# meh
class StatCounter(pygame.sprite.Sprite):
    total_points = 0
    temp = 0  # if its changed, temp changes to 1 (slightly speeds up)
    pointstr = "Score"

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.font = pygame.font.Font(globalvars.default_font,
                                     globalvars.points_text_size)
        self.rect = pygame.Rect(globalvars.points_x,
                                globalvars.points_y, 10, 10)  # TODO: ? change
        self.textimg = self.font.render(self.pointstr, 0, (255, 255, 0))
        self.textrect = self.textimg.get_rect()
        self.pointsimg = self.font.render(str(self.total_points), 0,
                                          (128, 128, 128))
        self.pointsrect = self.pointsimg.get_rect()
        self.pointsrect.move_ip(0, self.textrect.height)
        self.image = pygame.Surface(
            (self.textrect.width,
             self.pointsrect.height + self.textrect.height))
        # self.image.set_alpha(100)
        pygame.Surface.blit(self.image, self.textimg, self.textrect)
        pygame.Surface.blit(self.image, self.pointsimg, self.pointsrect)
        temp = 1

    def add_points(self, amount):
        self.total_points += amount
        self.temp = 1

    def set_points(self, amount):
        self.total_points = amount
        self.temp = 1

    def get_points(self):
        return self.total_points

    def sub_points(self, amount):
        self.total_points -= amount
        self.temp = 1

    def update(self):
        if self.temp != 0:
            self.image.fill(globalvars.bg_color, self.pointsrect)
            self.pointsimg = self.font.render(str(self.total_points),
                                              0, (255, 255, 255))
            self.pointsrect = self.pointsimg.get_rect()
            self.pointsrect.move_ip(0, self.textrect.height)
            pygame.Surface.blit(self.image, self.pointsimg,
                                self.pointsrect)
            self.temp = 0

    # def draw(self, screen):
        # text = self.font.render(self.pointstr + str(self.total_points),
                                # 0, (255, 255, 255))
        # screen.fill((0, 0, 0), self.rect)
        # screen.blit(text, (globalvars.points_x, globalvars.points_y))


###################
# 2 pieces of text on 1 image
class HealthNeedle(pygame.sprite.Sprite):
    total_health = 100
    temp = 0  # if its changed, temp changes to 1 (slightly speeds up)
    healthstr = "Shield"

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.font = pygame.font.Font(globalvars.default_font,
                                     globalvars.points_text_size)
        self.rect = pygame.Rect(globalvars.health_x,
                                globalvars.health_y,
                                10, 20)  # TODO: ? change
        self.textimg = self.font.render(self.healthstr, 0, (0, 255, 0))
        self.textrect = self.textimg.get_rect()
        self.healthimg = self.font.render(str(self.total_health), 0,
                                          (128, 128, 128))
        self.healthrect = self.healthimg.get_rect()
        self.healthrect.move_ip(0, self.textrect.height)
        self.image = pygame.Surface(
            (self.textrect.width,
             self.healthrect.height + self.textrect.height))
        # self.image.set_alpha(100)
        pygame.Surface.blit(self.image, self.textimg, self.textrect)
        pygame.Surface.blit(self.image, self.healthimg, self.healthrect)
        temp = 1

    def add_health(self, amount):
        if amount < 0:
            print("WARNING in add_health: added negative number"
                  "so subtracting!")
        self.total_health += amount
        self.temp = 1

    def set_health(self, total_health):
        self.total_health = total_health
        self.temp = 1

    def get_health(self):
        return self.total_health

    def get_temp(self):
        return self.temp

    def get_size(self):
        return pygame.Rect.union(self.healthrect, self.textrect)

    def sub_health(self, amount):
        if amount < 0:
            print("WARNING in sub_health: subtracted negative number"
                  "so adding!")
        self.total_health = self.total_health - amount
        self.temp = 1

    def hit(self, amount=1):
        self.sub_health(amount)

    def update(self):
        if self.temp != 0:
            self.image.fill(globalvars.bg_color, self.healthrect)
            self.healthimg = self.font.render(str(self.total_health), 0,
                                              (255, 255, 255))
            self.healthrect = self.healthimg.get_rect()
            self.healthrect.move_ip(0, self.textrect.height)
            pygame.Surface.blit(self.image, self.healthimg,
                                self.healthrect)
            # print("Health Decreased to " + str(self.total_health))
            self.temp = 0

    # def draw(self, screen):
        # text = self.font.render(str(self.total_health), 0,
                                # (255, 255, 255))
        # screen.fill((0, 0, 0), self.rect)
        # screen.blit(text, (globalvars.points_x, globalvars.points_y))


class Hud(pygame.sprite.Sprite):
    offset = globalvars.healthbar_offset_y
    offsetx = globalvars.healthbar_offset_x
    total_health = HealthNeedle.total_health
    width = globalvars.healthbar_width
    temp = HealthNeedle.temp  # if its changed, temp changes to 1, so it
    #                         # doesn't update every frame

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.healthneedle = HealthNeedle()
        self.top = self.healthneedle.get_size().bottom
        self.rect = pygame.Rect(self.offsetx, self.offset + self.top,
                                5, 110)  # TODO: ? change
        self.image = pygame.Surface((self.width, 110))
        h_rect = pygame.Rect(0, 0, self.width, self.total_health)
        pygame.draw.rect(self.image, (255, 255, 255), h_rect)

    def update(self):
        self.temp = self.healthneedle.get_temp()
        # print(HealthNeedle.total_health)
        if self.temp != 0:
            if self.total_health < self.healthneedle.get_health():
                max_h_rect = pygame.Rect(0, 0, self.width,
                                         globalvars.max_health)
                pygame.draw.rect(self.image, (128, 128, 128),
                                 max_h_rect)
            self.total_health = self.healthneedle.get_health()
            h_rect = pygame.Rect(
                0, 0, self.width,
                globalvars.max_health-self.total_health
            )
            pygame.draw.rect(self.image, globalvars.bg_color, h_rect)
            # print("Health Bar Decreased to"+str(self.total_health))
