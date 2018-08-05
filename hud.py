"""hud for pylaga

Blah. the display. StatCounter, Hud and HealthBar
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

    def __init__(self, rect, font_size=14, font_name="freesansbold.ttf",
                 bg_color=(0, 0, 0), aa=True):
        super(StatCounter, self).__init__()  # initialize sprite
        self.total_points = 0
        self.is_dirty = False  # if True, change graphics
        self.pointstr = "Score"
        self.aa = aa
        self.bg_color = bg_color
        self.font_size = font_size
        self.font = pygame.font.Font(font_name, self.font_size)
        self.rect = rect
            # TODO: ? change
        self.caption_img = self.font.render(self.pointstr,
                                            self.aa,
                                            (255, 255, 0))
        self.caption_rect = self.caption_img.get_rect()
        self.pointsimg = self.font.render(str(self.total_points),
                                          self.aa,
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
        self.is_dirty = True

    def add_points(self, amount):
        self.total_points += amount
        self.is_dirty = True

    def set_points(self, amount):
        self.total_points = amount
        self.is_dirty = True

    def get_points(self):
        return self.total_points

    def sub_points(self, amount):
        self.total_points -= amount
        self.is_dirty = True

    def update(self):
        if self.is_dirty is True:
            self.image.fill(self.bg_color, self.pointsrect)
            self.pointsimg = self.font.render(str(self.total_points),
                                              self.aa, (255, 255, 255))
            self.pointsrect = self.pointsimg.get_rect()
            self.pointsrect.move_ip(0, self.caption_rect.height)
            pygame.Surface.blit(self.image, self.pointsimg,
                                self.pointsrect)
            self.is_dirty = False

    # def draw(self, screen):
        # text = self.font.render(self.pointstr +
        #                         str(self.total_points),
        #                         self.aa, (255, 255, 255))
        # screen.fill((0, 0, 0), self.rect)
        # screen.blit(text, self.rect.topleft)


###################
# 2 pieces of text on 1 image
class HealthBar(pygame.sprite.Sprite):

    def __init__(self, health, text_color, font_size=14,
                 font_name="freesansbold.ttf",
                 bg_color=(0, 0, 0), aa=True):
        super(HealthBar, self).__init__()  # initialize sprite
        self.aa = aa
        self.bg_color = bg_color
        self.is_dirty = False  # if True, change graphics
        self.healthstr = "Shield"
        self.health = health
        self.font_size = font_size
        self.text_color = text_color
        self.font = pygame.font.Font(font_name, self.font_size)
        self.rect = pygame.Rect(0, 50, 10, 20)
        self.caption_img = self.font.render(self.healthstr,
                                            self.aa, (0, 255, 0))
        self.caption_rect = self.caption_img.get_rect()
        self.healthimg = self.font.render(str(self.health), self.aa,
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
        is_dirty = True

    def add_health(self, amount):
        if amount < 0:
            print("WARNING in add_health: added negative number"
                  "so subtracting!")
        self.health += amount
        self.is_dirty = True

    def set_health(self, health):
        self.health = health
        self.is_dirty = True

    def get_health(self):
        return self.health

    def get_is_dirty(self):
        return self.is_dirty

    def get_dest_rect(self):
        return pygame.Rect.union(self.healthrect, self.caption_rect)

    def set_health(self, health):
        if health != self.health:
            self.is_dirty = True
        self.health = health

    def update(self):
        if self.is_dirty is True:
            self.image.fill(self.bg_color, self.healthrect)
            self.healthimg = self.font.render(str(self.health), self.aa,
                                              self.text_color)
            self.healthrect = self.healthimg.get_rect()
            self.healthrect.move_ip(0, self.caption_rect.height)
            pygame.Surface.blit(self.image, self.healthimg,
                                self.healthrect)
            # print("Health Decreased to " + str(self.health))
            self.is_dirty = False

    # def draw(self, screen):
        # text = self.font.render(str(self.health), self.aa,
                                # (255, 255, 255))
        # screen.fill((0, 0, 0), self.rect)
        # screen.blit(text, self.rect.topleft)


class Hud(pygame.sprite.Sprite):

    def __init__(self, rect, bg_color, fg_color, max_health):
        super(Hud, self).__init__()  # initialize sprite
        self.rect = rect
        self.healthbar = HealthBar(max_health, fg_color)
        self.health = self.healthbar.health
        self.rect.top = self.healthbar.get_dest_rect().bottom
        self.rect.height -= self.healthbar.get_dest_rect().height
        self.max_health = max_health
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        h_rect = pygame.Rect(0, 0, self.rect.width, self.health)
        pygame.draw.rect(self.image, self.fg_color, h_rect)


    def update(self):
        # print("health: " + str(self.health))
        if self.healthbar.get_is_dirty():
            if self.health != self.healthbar.get_health():
                max_h_rect = pygame.Rect(0, 0, self.rect.width,
                                         self.max_health)
                pygame.draw.rect(self.image, self.fg_color,
                                 max_h_rect)
                self.health = self.healthbar.get_health()
            h_rect = pygame.Rect(0, 0, self.rect.width,
                                 self.max_health-self.health)
            pygame.draw.rect(self.image, self.bg_color, h_rect)
            # print("Health Bar Decreased to" + str(self.total_health))
