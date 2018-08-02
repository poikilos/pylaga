# 2007-04-1 RJ Marsan
# Pylaga
# Original: 2007-02-20 Derek Mcdonald
# Subclass of pylaga.py
#
#  Blah. the display. points, health and healthbar
# TODO: Eliminate global vars:
#       This whole file needs to be cleaned up to adhere to the
#    globalvars more, I'm lazy.
#    Scratch that. we need to get rid of globalvars altogether.
#    DEATH TO GLOBAL VARS!
#
import pygame
import os
import sys
import math
import random
import globalvars


###################
# TODO: i needed to make this an object because i couldnt figure out how
# to make it globally available but also writable
# meh
class Points(pygame.sprite.Sprite):
    total_points = 0
    temp = 0  # if its changed, temp changes to 1 (slightly speeds up)
    pointstr = "Score"

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.font = pygame.font.Font(globalvars.defaultfont,
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

    def add_points(self, points):
        self.total_points += points
        self.temp = 1

    def set_points(self, points):
        self.total_points = points
        self.temp = 1

    def get_points(self):
        return self.total_points

    def sub_points(self, points):
        self.total_points -= points
        self.temp = 1

    def update(self):
        if self.temp != 0:
            self.image.fill(globalvars.bgcolor, self.pointsrect)
            self.pointsimg = self.font.render(str(self.total_points),
                                              0, (255, 255, 255))
            self.pointsrect = self.pointsimg.get_rect()
            self.pointsrect.move_ip(0, self.textrect.height)
            pygame.Surface.blit(self.image, self.pointsimg,
                                self.pointsrect)
            self.temp = 0

    def draw(self):
        text = self.font.render(self.pointstr + str(self.total_points),
                                0, (255, 255, 255))
        globalvars.surface.fill((0, 0, 0), self.rect)
        globalvars.surface.blit(text,
                                (globalvars.points_x,
                                 globalvars.points_y))


###################
# 2 pieces of text on 1 image
class Health(pygame.sprite.Sprite):
    total_health = 100
    temp = 0  # if its changed, temp changes to 1 (slightly speeds up)
    healthstr = "Shield"

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.font = pygame.font.Font(globalvars.defaultfont,
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

    def add_health(self, health):
        self.total_health += points
        self.temp = 1

    def set_health(self, health):
        self.total_health = health
        self.temp = 1

    def get_health(self):
        return self.total_health

    def get_temp(self):
        return self.temp

    def get_size(self):
        return pygame.Rect.union(self.healthrect, self.textrect)

    def sub_health(self, health):
        self.total_health = self.total_health - (health)
        # print("hit " + str(self.total_health))
        self.temp = 1

    def hit(self):
        self.sub_health(1)

    def update(self):
        if self.temp != 0:
            self.image.fill(globalvars.bgcolor, self.healthrect)
            self.healthimg = self.font.render(str(self.total_health), 0,
                                              (255, 255, 255))
            self.healthrect = self.healthimg.get_rect()
            self.healthrect.move_ip(0, self.textrect.height)
            pygame.Surface.blit(self.image, self.healthimg,
                                self.healthrect)
            # print("Health Decreased to " + str(self.total_health))
            self.temp = 0

    def draw(self):
        text = self.font.render(str(self.total_health), 0,
                                (255, 255, 255))
        globalvars.surface.fill((0, 0, 0), self.rect)
        globalvars.surface.blit(text, (globalvars.points_x,
                                       globalvars.points_y))


class HealthBar(pygame.sprite.Sprite):
    offset = globalvars.healthbar_offset_y
    offsetx = globalvars.healthbar_offset_x
    total_health = Health.total_health
    width = globalvars.healthbar_width
    temp = Health.temp  # if its changed, temp changes to 1, so it
    #                   # doesn't update every frame

    def __init__(self, health):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.top = health.get_size().bottom
        self.rect = pygame.Rect(self.offsetx, self.offset + self.top,
                                5, 110)  # TODO: ? change
        self.image = pygame.Surface((self.width, 110))
        h_rect = pygame.Rect(0, 0, self.width, self.total_health)
        pygame.draw.rect(self.image, (255, 255, 255), h_rect)
        self.healthobject = health

    def update(self):
        self.temp = self.healthobject.get_temp()
        # print(Health.total_health)
        if self.temp != 0:
            if self.total_health < self.healthobject.get_health():
                max_h_rect = pygame.Rect(0, 0, self.width,
                                         globalvars.max_health)
                pygame.draw.rect(self.image, (128, 128, 128), max_h_rect)
            self.total_health = self.healthobject.get_health()
            h_rect = pygame.Rect(
                0, 0, self.width,
                globalvars.max_health-self.total_health
            )
            pygame.draw.rect(self.image, globalvars.bgcolor, h_rect)
            # print("Health Bar Decreased to"+str(self.total_health))

#####################
global points
points = Points()
globalvars.side_panel.add(points)
global health
health = Health()
global healthbar
healthbar = HealthBar(health)
globalvars.side_panel.add(healthbar)
globalvars.side_panel.add(health)
