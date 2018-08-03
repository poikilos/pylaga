"""hud for pylaga

Blah. the display. StatCounter, Hud and HealthNeedle
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

###################
# TODO: i needed to make this an object because i couldnt figure out how
# to make it globally available but also writable
# meh
class StatCounter(pygame.sprite.Sprite):
    total_points = 0
    tmpr = 0  # if above 0, don't do periodic calculations
    pointstr = "Score"

    def __init__(self, rect, font_size=14, font_name="freesansbold.ttf",
                 bg_color=(0, 0, 0)):
        self.bg_color = bg_color
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.font_size = font_size
        self.font = pygame.font.Font(font_name, self.font_size)
        self.rect = rect
            # TODO: ? change
        self.caption_img = self.font.render(self.pointstr, 0,
                                            (255, 255, 0))
        self.caption_rect = self.caption_img.get_rect()
        self.pointsimg = self.font.render(str(self.total_points), 0,
                                          (128, 128, 128))
        self.pointsrect = self.pointsimg.get_rect()
        self.pointsrect.move_ip(0, self.caption_rect.height)
        self.image = pygame.Surface(
            (self.caption_rect.width,
             self.pointsrect.height + self.caption_rect.height))
        # self.image.set_alpha(100)
        pygame.Surface.blit(self.image, self.caption_img,
                            self.caption_rect)
        pygame.Surface.blit(self.image, self.pointsimg, self.pointsrect)
        self.tmpr = 1

    def add_points(self, amount):
        self.total_points += amount
        self.tmpr = 1

    def set_points(self, amount):
        self.total_points = amount
        self.tmpr = 1

    def get_points(self):
        return self.total_points

    def sub_points(self, amount):
        self.total_points -= amount
        self.tmpr = 1

    def update(self):
        if self.tmpr != 0:
            self.image.fill(self.bg_color, self.pointsrect)
            self.pointsimg = self.font.render(str(self.total_points),
                                              0, (255, 255, 255))
            self.pointsrect = self.pointsimg.get_rect()
            self.pointsrect.move_ip(0, self.caption_rect.height)
            pygame.Surface.blit(self.image, self.pointsimg,
                                self.pointsrect)
            self.tmpr = 0

    # def draw(self, screen):
        # text = self.font.render(self.pointstr +
        #                         str(self.total_points),
        #                         0, (255, 255, 255))
        # screen.fill((0, 0, 0), self.rect)
        # screen.blit(text, self.rect.topleft)


###################
# 2 pieces of text on 1 image
class HealthNeedle(pygame.sprite.Sprite):

    def __init__(self, health, text_color, font_size=14,
                 font_name="freesansbold.ttf",
                 bg_color=(0, 0, 0)):
        self.bg_color = bg_color
        self.tmpr = 0  # if above 0, don't do periodic calculations
        self.healthstr = "Shield"
        self.health = health
        self.font_size = font_size
        self.text_color = text_color
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.font = pygame.font.Font(font_name, self.font_size)
        self.rect = pygame.Rect(0, 50, 10, 20)
        self.caption_img = self.font.render(self.healthstr,
                                            0, (0, 255, 0))
        self.caption_rect = self.caption_img.get_rect()
        self.healthimg = self.font.render(str(self.health), 0,
                                          (128, 128, 128))
        self.healthrect = self.healthimg.get_rect()
        self.healthrect.move_ip(0, self.caption_rect.height)
        self.image = pygame.Surface(
            (self.caption_rect.width,
             self.healthrect.height + self.caption_rect.height))
        # self.image.set_alpha(100)
        pygame.Surface.blit(self.image, self.caption_img,
                            self.caption_rect)
        pygame.Surface.blit(self.image, self.healthimg, self.healthrect)
        tmpr = 1

    def add_health(self, amount):
        if amount < 0:
            print("WARNING in add_health: added negative number"
                  "so subtracting!")
        self.health += amount
        self.tmpr = 1

    def set_health(self, health):
        self.health = health
        self.tmpr = 1

    def get_health(self):
        return self.health

    def get_temper(self):
        return self.tmpr

    def get_dest_rect(self):
        return pygame.Rect.union(self.healthrect, self.caption_rect)

    def sub_health(self, amount):
        if amount < 0:
            print("WARNING in sub_health: subtracted negative number"
                  "so adding!")
        self.health -= amount
        self.tmpr = 1

    def hit(self, amount=1):
        self.sub_health(amount)

    def update(self):
        if self.tmpr != 0:
            self.image.fill(self.bg_color, self.healthrect)
            self.healthimg = self.font.render(str(self.health), 0,
                                              self.text_color)
            self.healthrect = self.healthimg.get_rect()
            self.healthrect.move_ip(0, self.caption_rect.height)
            pygame.Surface.blit(self.image, self.healthimg,
                                self.healthrect)
            # print("Health Decreased to " + str(self.health))
            self.tmpr = 0

    # def draw(self, screen):
        # text = self.font.render(str(self.health), 0,
                                # (255, 255, 255))
        # screen.fill((0, 0, 0), self.rect)
        # screen.blit(text, self.rect.topleft)


class Hud(pygame.sprite.Sprite):

    def __init__(self, rect, bg_color, fg_color, max_health):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.rect = rect
        self.healthneedle = HealthNeedle(max_health, fg_color)
        # if health changed, tmpr changes to 1,
        # so health doesn't decrease every frame
        self.health = self.healthneedle.health
        self.rect.top = self.healthneedle.get_dest_rect().bottom
        self.rect.height -= self.healthneedle.get_dest_rect().height
        self.max_health = max_health
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        h_rect = pygame.Rect(0, 0, self.rect.width, self.health)
        pygame.draw.rect(self.image, self.fg_color, h_rect)


    def update(self):
        # print(self.health)
        if self.healthneedle.get_temper() != 0:
            if self.health != self.healthneedle.get_health():
                max_h_rect = pygame.Rect(0, 0, self.rect.width,
                                         self.max_health)
                pygame.draw.rect(self.image, self.fg_color,
                                 max_h_rect)
                self.health = self.healthneedle.get_health()
            h_rect = pygame.Rect(0, 0, self.rect.width,
                                 self.max_health-self.health)
            pygame.draw.rect(self.image, self.bg_color, h_rect)
            # print("Health Bar Decreased to" + str(self.total_health))
