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


class Blip(pygame.sprite.Sprite):
    """Widget for the Hud

    Blip stores values and can have a bar, value, or caption enabled,
    or theoretically have none enabled in which case the blip would be
    invisible but could still serve as a value to be accessed
    such as using a Hud's get_blip_value method.
    """

    def __init__(self, pos, max_val, max_bar_length,
                 text_color=(255, 255, 255),
                 font_size=14,
                 font_name="freesansbold.ttf",
                 bg_color=(0, 0, 0),
                 fg_color=(255, 255, 255), caption=None,
                 aa=True,
                 bar_enable=True,
                 value_enable=True, orientation='v'):
        super(Blip, self).__init__()  # initialize sprite
        self.orientation = orientation
        self.bar_enable = bar_enable
        self.value_enable = value_enable
        caption_enable = caption is not None
        self.caption = caption
        self.aa = aa
        self.max_bar_rect = None
        bar_w = 5  # bar width aka bar_width
        if self.bar_enable:
            if self.orientation == 'v':
                self.max_bar_rect = pygame.Rect(0, 0, bar_w,
                                                max_bar_length)
            else:
                self.max_bar_rect = pygame.Rect(0, 0, max_bar_length, 5)
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.is_dirty = True  # if True, change graphics
        self.max_val = max_val
        self.val = max_val
        self.font_size = font_size
        self.text_color = text_color
        self.font = pygame.font.Font(font_name, self.font_size)
        self.rect = pygame.Rect(0, 0, 0, 0)  # outline, moved below
        if caption_enable:
            self.caption_img = self.font.render(self.caption,
                                                self.aa, text_color)
            self.caption_rect = self.caption_img.get_rect()
            self.rect = pygame.Rect.union(self.rect, self.caption_rect)
        else:
            self.caption_img = None
            self.caption_rect = pygame.Rect(0, 0, 0, 0)
        if value_enable:
            self.value_img = self.font.render(str(self.val), self.aa,
                                              (128, 128, 128))
            self.value_rect = self.value_img.get_rect()
            x = 0
            if self.caption_rect.width > 0:
                # x = (self.caption_rect.centerx -
                     # self.value_rect.width / 2)
                x = 12  # so all bars are on same x, don't calculate
            self.value_rect.move_ip(x, self.caption_rect.height)
            self.rect = pygame.Rect.union(self.rect, self.value_rect)
        else:
            self.value_img = None
            self.value_rect = pygame.Rect(0, 0, 0, 0)

        max_w = max(self.caption_rect.width, self.value_rect.width)
        if self.bar_enable:
            if self.orientation != 'v':
                self.max_bar_rect.move_ip(max_w / 2 -
                                          self.max_bar_rect.width,
                                          self.rect.bottom)
            else:
                x = 0
                if self.caption_rect.width > 0:
                    # x = (self.caption_rect.centerx -
                         # self.value_rect.width / 2)
                    x = 12  # so all bars are on same x, don't calculate
                self.max_bar_rect.move_ip(x, self.rect.bottom)
            self.bar_rect = self.max_bar_rect.copy()
            self.rect = pygame.Rect.union(self.rect, self.bar_rect)
            print("created bar " + self.caption + " with bar: " +
                  str(self.bar_rect))

        self.image = pygame.Surface(self.rect.size)

        if caption_enable:
            pygame.Surface.blit(self.image, self.caption_img,
                                self.caption_rect)
        if self.value_enable:
            pygame.Surface.blit(self.image, self.value_img,
                                self.value_rect)
        self.rect.move_ip(pos)
        self.update_bar()
        is_dirty = True

    def get_caption_enable(self):
        return self.caption is not None

    def update_bar(self):
        if not self.bar_enable:
            return
        if self.orientation == 'v':
            pygame.draw.rect(self.image, self.bg_color,
                             self.max_bar_rect)
            # "Assigning to size, width or height changes the dimensions
            # of the rectangle; all other assignments move the rectangle
            # without resizing it." - pygame docs 2018-08-06
            self.bar_rect.height = int(round((self.val /
                                              self.max_val ) *
                                       self.max_bar_rect.height))
            self.bar_rect.bottom = self.max_bar_rect.bottom
        else:
            pygame.draw.rect(self.image, self.bg_color,
                             self.max_bar_rect)
            self.bar_rect.width = int(round((self.val /
                                             self.max_val ) *
                                      self.max_bar_rect.width))
            # no need to move rect, starts at left
        pygame.draw.rect(self.image, self.fg_color, self.bar_rect)

    def add_value(self, amount):
        if amount < 0:
            print("WARNING in add_health: added negative number"
                  "so subtracting!")
        elif amount > 0:
            self.val += amount
            self.is_dirty = True
            self.update_bar()

    def set_v(self, val):
        if val != self.val:
            self.is_dirty = True
            self.update_bar()
        self.val = val

    def get_v(self):
        return self.val

    def get_is_dirty(self):
        return self.is_dirty

    def get_dest_rect(self):
        return pygame.Rect.union(self.value_rect, self.caption_rect)

    def update(self):
        if self.is_dirty is True:
            if self.value_enable:
                self.image.fill(self.bg_color, self.value_rect)
                self.value_img = self.font.render(str(self.val),
                                                  self.aa,
                                                  self.text_color)
                new_v_rect = self.value_img.get_rect()
                self.value_rect.width = new_v_rect.width
                self.value_rect.height = new_v_rect.height
                # if self.get_caption_enable():
                    # NOTE: coords for self.image, not screen:
                    # self.value_rect.move_ip(0,
                    #                         self.caption_rect.height)
                pygame.Surface.blit(self.image, self.value_img,
                                    self.value_rect)
            self.update_bar()
            self.is_dirty = False

    # def draw(self, screen):
        # text = self.font.render(str(self.val), self.aa,
                                # (255, 255, 255))
        # screen.fill((0, 0, 0), self.rect)
        # screen.blit(text, self.rect.topleft)


class Hud(pygame.sprite.Group):

    def __init__(self):
        super(Hud, self).__init__()  # initialize spritegroup
        self.default_bar_h = 100
        self.bg_color = (64, 64, 64)
        self.fg_color = (255, 255, 255)
        self.blips = {}  # dict of Blips
        self.rect = pygame.Rect(0, 0, 1, 1)

    def generate_blip(self, name, max_v, bar_enable=True,
            bg_color=None, fg_color=None, text_color=None,
            caption=None):
        if caption is None:
            caption = name[0].upper() + name[1:].lower()
        next_y = 0
        if bg_color is None:
            bg_color = (0, 0, 0)
        if fg_color is None:
            fg_color = (255, 255, 255)
        if text_color is None:
            text_color = (255, 255, 255)
        print("adding blip to blips: " + str(self.blips))
        for key, blip in self.blips.items():
            next_y += blip.rect.height
        new_blip = Blip((0, next_y), max_v,
                        self.default_bar_h,
                        text_color=text_color,
                        fg_color=fg_color,
                        bar_enable=bar_enable,
                        caption=caption)
        self.blips[name] = new_blip
        if self.rect is None:
            self.rect = self.new_blip.rect.copy()
        else:
            self.rect = pygame.Rect.union(self.rect, new_blip.rect)
        self.add(new_blip)  # add to spritegroup so gets drawn

    def set_blip_value(self, name, v):
        self.blips[name].set_v(v)

    def get_blip_value(self, name):
        return self.blips[name].get_v()

    def get_blip(self, name):
        return self.blips[name]

    def update(self):
        for key, blip in self.blips.items():
            blip.update()
