"""generic menu class

Its a generic menu object, it takes 1 parameter, and thats an
array of strings to display.
Menus are managed by the menulists module.
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

# takes a tuple of menuitem strings as input
# a generic menu class
# very effective
class Menu:

    def __init__(self, menu_strings, menus):
        self.menus = menus
        self.cursor_image = self.menus.cursor_image
        self.font_rect_height = None
        self.shipselectorsize = 50, 50  # updated before use
        self.font_size = 20  # these do fairly obvious things
        self.offset_x = 100
        self.offset_y = 200
        self.spacing = 10
        self.selection = 0
        self.font = pygame.font.Font(globalvars.default_font,
                                     self.font_size)
        self.menuimgs = []
        self.menurects = []
        x = 0
        w, h = menus.screen.get_size()
        for entry_s in menu_strings:
                # render all the strings that were received
            menuimg = self.font.render(entry_s, 1,
                                       globalvars.menu_color)
            menurect = menuimg.get_rect()
            if len(self.menuimgs) < 1:  # if not self.menuimgs:
                self.font_rect_height = menurect.height
                self.update_selector_size()
                self.spacing = int(h / 60)
                self.offset_x = (w - menurect.width) / 2
                self.offset_y = int(h / 2 +
                                    self.shipselectorsize[1] +
                                    self.spacing)
                menurect.move_ip(self.offset_x, self.offset_y)
            else:
                menurect.move_ip(
                    self.offset_x,
                    self.menurects[x-1].bottom+self.spacing
                )
            self.menuimgs.append(menuimg)
            self.menurects.append(menurect)
            x += 1

        self.menurect = pygame.Rect(
            self.menurects[0].topleft,
            self.menurects[len(self.menurects)-1].bottomright
        )
        self.selectedrect = pygame.Rect(
            self.menurect.left-self.shipselectorsize[0]-self.spacing,
            self.menurect.top,
            self.shipselectorsize[0],
            self.menurect.height
        )
        self.selectedimg = pygame.Surface(self.selectedrect.size)
        self.shipimg = pygame.transform.rotate(self.cursor_image,
                                               0)  # -90)
        self.shipimg = pygame.transform.scale(
            self.cursor_image,
            (self.shipselectorsize[0], self.shipselectorsize[1])
        )
        self.offset_y = self.menurects[0].height + self.spacing
        cursor_rect = pygame.Rect(0, self.selection*self.offset_y,
                                  self.shipselectorsize[0],
                                  self.shipselectorsize[1])
        self.selectedimg.blit(self.shipimg, cursor_rect)
        x = 0
        self.menus.screen.blit(self.menus.logo_image,
                               self.menus.logo_image.get_rect())
        for menuimg in self.menuimgs:
                # draw all the images to the display
            self.menus.screen.blit(menuimg, self.menurects[x])
            x += 1
        self.menus.screen.blit(self.selectedimg, self.selectedrect)
        pygame.display.flip()

    def update_selector_size(self):
        if self.font_rect_height is not None:
            # intentionally make a square using font height
            self.shipselectorsize = (int(self.font_rect_height),
                                     int(self.font_rect_height))

    # generic selection changing class, not really used by outside
    # unless they know what they're doing
    def change_selection(self, selection):
        self.selectedimg.fill(globalvars.bg_color)
        self.update_selector_size()
        cursor_rect = pygame.Rect(0, selection*self.offset_y,
                                  self.shipselectorsize[0],
                                  self.shipselectorsize[1])
        self.selectedimg.blit(self.shipimg, cursor_rect)
        self.menus.screen.blit(self.selectedimg, self.selectedrect)
        pygame.display.update(self.selectedrect)

    # simple methods to move selction up or down
    def change_selection_up(self):
        if self.selection > 0:
            self.selection -= 1
        self.change_selection(self.selection)

    def change_selection_down(self):
        if self.selection < len(self.menurects):
            self.selection += 1
        self.change_selection(self.selection)

    # a mouse oritened change_selection
    def change_selection_pos(self, pos):
        changed = False
        x = 0
        for menu_rect in self.menurects:
            if menu_rect.collidepoint(pos):
                if self.selection != x:
                    self.selection = x
                    changed = True
            x += 1
        if changed:
            self.change_selection(self.selection)

    # useful so that a random mouseclick doesnt do anything
    def mouse_is_anywhere(self, pos):
        for menu_rect in self.menurects:
            if menu_rect.collidepoint(pos):
                return True
        return False

    # returns selection (duh)
    def get_selection(self):
        return self.selection

# TODO: other screens

    def disp_about(self):
        menus.page = 'about'
        return

    def disp_help(self):
        menus.page = 'help'
        return
