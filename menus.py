"""menu manager for pylaga

A few premade menu objects
Makes it easier on my brain
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
from menu import Menu

# takes a tuple of menuitem strings as input
# a generic menu class
# very effective
# The app param must at least contain the following pygame objects:
# app.clock app.screen
class Menus:
    # region the menu functions

    def __init__(self, statcounter, app, logo_image, cursor_image,
                 bg_color=(0, 0, 0)):
        self.bg_color = bg_color
        self._vars = {}
        self.page = 'top'
        self.statcounter = statcounter
        self.app = app
        self.screen = app.screen
        self.logo_image = logo_image
        self.cursor_image = cursor_image

    def init_menu(self):
        self.clear_screen()
        menu = Menu(("PLAY", "ABOUT", "HELP", "EXIT"), self)
        selection = -1
        while True:
            events = pygame.event.get()
            selection = self.menu_action(events, menu)
            if selection >= 0:
                if selection == 0:
                    break
                if selection == 1:
                    menu.disp_about()
                if selection == 2:
                    menu.disp_help()
                if selection == 3:  # Chose EXIT
                    self.set_bool('exit', True)
                    break
                    # fall through to on_exit handler
            self.app.clock.tick(self.app.get_fps())
        self.clear_screen()
        pygame.mouse.set_visible(0)
        pygame.event.set_grab(not self.get_bool('exit'))

    def get_bool(self, name):
        return self._vars.get(name)

    def set_bool(self, name, v):
        self._vars[name] = v is True

    def exit_menu(self):
        self.clear_screen()
        pygame.mouse.set_visible(1)
        menu = Menu(("RETRY", "ABOUT", "HELP", "EXIT",
                     "Score: %s" % self.statcounter.get_points()),
                    self)
        selection = -1
        while True:
            events = pygame.event.get()
            selection = self.menu_action(events, menu)
            if selection >= 0:
                if selection == 0:
                    break
                if selection == 1:
                    menu.disp_about()
                if selection == 2:
                    menu.disp_help()
                if selection == 3:
                    self.set_bool('exit', True)
                    return False
            self.app.clock.tick(self.app.get_fps())
        self.clear_screen()
        pygame.mouse.set_visible(0)
        return True

    def pause_menu(self):
        self.clear_screen()
        pygame.mouse.set_visible(1)
        pygame.event.set_grab(False)
        menu = Menu(("RESUME", "ABOUT", "HELP", "EXIT"),
                    self)
        selection = -1
        while True:
            events = pygame.event.get()
            selection = self.menu_action(events, menu)
            if selection >= 0:
                if selection == 0:
                    break
                if selection == 1:
                    menu.disp_about()
                if selection == 2:
                    menu.disp_help()
                if selection == 3:
                    self.set_bool('exit', True)
                    break
                    # fall through to on_exit handler
            self.app.clock.tick(self.app.get_fps())
        self.clear_screen()
        pygame.mouse.set_visible(0)
        pygame.event.set_grab(not self.get_bool('exit'))

    def menu_action(self, events, menu):
        selection = -1
        pygame.event.pump()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit(0)
                # if event.key == pygame.K_ESCAPE:
                    # sys.exit(0)
                if event.key == pygame.K_UP:
                    menu.change_selection_up()
                if event.key == pygame.K_DOWN:
                    menu.change_selection_down()
                if event.key == pygame.K_RETURN:
                    selection = menu.get_selection()
            if event.type == pygame.MOUSEMOTION:
                menu.change_selection_pos(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu.change_selection_pos(event.pos)
                if menu.mouse_is_anywhere(event.pos):
                    selection = menu.get_selection()
        return selection
    # endregion the menu functions

    def clear_screen(self):
        self.screen.fill(self.bg_color)
        pygame.display.flip()
