"""generic menu class

Its a generic menu object, it takes 1 parameter, and thats an
array of strings to display.
Menus are managed by the menus module.
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
import time

# takes a tuple of menuitem strings as input
# a generic menu class
# very effective
class Menu:

    def __init__(self, menu_strings, menus, font_size=20,
                 font_name="freesansbold.ttf",
                 readable_font_name="freesansbold.ttf",
                 readable_font_size=14,
                 fg_color=(195, 227, 247),
                 bg_color=(0, 0, 0),
                 aa=True):
        print("creating menu: " + str(menu_strings))
        self.menu_strings = menu_strings
        self.delay_count = 0  # waiting to show lines of scrolling text
        self.aa = aa
        self.page_name = None
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.menus = menus
        self.cursor_image = self.menus.cursor_image
        self.cursor_spin = 0.0
        self.cursor_start_angle = 0.0
        self.cursor_angle = self.cursor_start_angle
        self.font_rect_height = None
        self.shipselectorsize = 50, 50  # updated before use
        self.font_size = font_size
        self.offset_x = 100
        self.offset_y = 200
        self.spacing = 10
        self.result_i = -1
        self.select_i = -1
        self.readable_font_name = readable_font_name
        self.readable_font_size = readable_font_size
        self.readable_font = pygame.font.Font(self.readable_font_name,
                                              self.readable_font_size)
        self.font = pygame.font.Font(font_name, self.font_size)
        self.draw_menu_buttons(menu_strings, None)

    def draw_menu_buttons(self, menu_strings, page_name, top=None,
            change_page=True):
        if menu_strings is not None:
            if menu_strings != self.menu_strings:
                self.result_i = -1
                self.select_i = 0
        self.entry_imgs = []
        self.menu_rects = []
        if menu_strings is not None:
            self.menu_strings = menu_strings
        self.menus.screen.fill(self.bg_color)
        i = 0
        w, h = self.menus.screen.get_size()
        for entry_s in self.menu_strings:
            # render all the strings that were received
            entry_img = self.font.render(entry_s, self.aa,
                                         self.fg_color)
            menurect = entry_img.get_rect()
            if len(self.entry_imgs) < 1:  # if not self.entry_imgs:
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
                    self.menu_rects[i-1].bottom+self.spacing
                )
            self.entry_imgs.append(entry_img)
            self.menu_rects.append(menurect)
            i += 1

        self.menurect = pygame.Rect(
            self.menu_rects[0].topleft,
            self.menu_rects[len(self.menu_rects)-1].bottomright
        )
        self.selectedrect = pygame.Rect(
            self.menurect.left-self.shipselectorsize[0]-self.spacing,
            self.menurect.top,
            self.shipselectorsize[0],
            self.menurect.height
        )
        self.selectedimg = pygame.Surface(self.selectedrect.size,
                                          pygame.SRCALPHA, 32)
        self.selectedimg.fill((80,80,32,0))
        # self.final_cursor = self.cursor_image
        self.final_cursor = pygame.transform.rotate(self.cursor_image,
                                               self.cursor_angle)
        self.cursor_angle += self.cursor_spin
        self.final_cursor = pygame.transform.scale(
            self.final_cursor,
            (self.shipselectorsize[0], self.shipselectorsize[1])
        )
        self.offset_y = self.menu_rects[0].height + self.spacing
        cursor_rect = pygame.Rect(0, self.select_i*self.offset_y,
                                  self.shipselectorsize[0],
                                  self.shipselectorsize[1])
        self.selectedimg.blit(self.final_cursor, cursor_rect)
        i = 0
        self.menus.screen.blit(self.menus.logo_image,
                               self.menus.logo_image.get_rect())
        for entry_img in self.entry_imgs:
            self.menus.screen.blit(entry_img, self.menu_rects[i])
            i += 1
        self.menus.screen.blit(self.selectedimg, self.selectedrect)
        if (page_name is not None) and (self.page_name != page_name):
            # scroll though if not yet drawn:
            print("begin scrolling text counter...")
            self.delay_count = 0
        delay = 10
        if change_page:
            self.page_name = page_name
        self.draw_scroll(self.menus.screen, delay=delay)
        # pygame.display.flip()

    def update_selector_size(self):
        if self.font_rect_height is not None:
            # intentionally make a square using font height
            self.shipselectorsize = (int(self.font_rect_height),
                                     int(self.font_rect_height))

    # generic selection changing class, not really used by outside
    # unless they know what they're doing
    def draw_cursor(self, screen):
        # self.draw_scroll(screen, delay=0)
        self.selectedimg.fill(self.bg_color)
        self.update_selector_size()
        cursor_rect = pygame.Rect(0, self.select_i*self.offset_y,
                                  self.shipselectorsize[0],
                                  self.shipselectorsize[1])
        self.selectedimg.blit(self.final_cursor, cursor_rect)
        screen.blit(self.selectedimg, self.selectedrect)
        # TODO: ? pygame.display.update(self.selectedrect)

    # simple methods to move selction up or down
    def change_selection_up(self, screen):
        if self.select_i > 0:
            self.select_i -= 1

    def change_selection_down(self, screen):
        if self.select_i < len(self.menu_rects):
            self.select_i += 1

    # a mouse-orientened change_selection
    def change_selection_pos(self, pos, screen):
        self.select_i = -1
        for i in range(len(self.menu_rects)):
            menu_rect = self.menu_rects[i]
            if menu_rect.collidepoint(pos):
                if self.select_i != i:
                    self.select_i = i
                    break

    def get_selection(self):
        ret = None
        if ((self.select_i is not None) and
                (self.select_i >= 0) and
                (self.select_i < len(self.menu_strings))):
            ret = self.menu_strings[self.select_i]
        return ret

    def get_selection_index(self):
        return self.select_i

    def draw_scroll(self, screen, delay=10):
        # if page_name is not None:
            # self.page_name = page_name
        pages_dict = self.menus.pages_dict
        msg = None
        page = pages_dict.get(self.page_name)
        if page is not None:
            msg = page.get('scroll_text')
        if msg is not None:
            count = 0
            if self.delay_count is None:
                print("WARNING in draw_scroll: initialized"
                      " delay_count automatically")
                self.delay_count = 0
            max_count = int(self.delay_count / delay)
            lines = msg.split("\n")
            dest_rect = pygame.Rect(10, 5, 1, 1)
            font = self.readable_font
            for line in lines:
                pygame.event.pump()
                # msg_img = font.render(line, self.aa, self.fg_color)
                # msg_rect = msg_img.get_rect()
                # dest_rect.width = msg_rect.width
                # dest_rect.height = msg_rect.height
                msg_rect = self.menus.render_bordered_to(
                    screen,
                    font,
                    line,
                    dest_rect.topleft
                )
                dest_rect.move_ip(0, msg_rect.height)
                # screen.blit(msg_img, dest_rect.topleft)
                # pygame.display.flip()
                count += 1
                if count >= max_count:
                    break
            # print("drew " + str(count))
            # print(" self.delay_count " + str(self.delay_count))
            # print(" of max_count " + str(max_count))
            # TODO: if count < len(lines):
            self.delay_count += 1

