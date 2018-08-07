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

# takes a form dict as input such as:
# pages_dict = {
#     "PLAY":{},
#     "ABOUT":{
#         "scroll_text":"WRITTEN BY\nauthor1\nauthor2\nauthor3"
#     }
# }
# if no pages_dict is specified, the buttons will do actions but not
# go to a separate screen
# a generic menu class
# very effective
# The app param must at least contain the following pygame objects:
# app.clock app.screen
class Menus:
    # region the menu functions

    def __init__(self, statcounter, app, logo_image, cursor_image,
                 pages_dict,
                 # about_string='', help_string='',
                 bg_color=(0, 0, 0)):
        self.bg_color = bg_color
        self.pages_dict = pages_dict
        about = pages_dict.get('ABOUT')
        about_string = None
        if about is not None:
            about_string = about.get('scroll_text')
        else:
            self.pages_dict['ABOUT'] = {}
        if len(about_string) < 1:
            try:
                self.pages_dict['ABOUT']['scroll_text'] = \
                    "author: " + __author__
            except:
                pass
        self._vars = {}
        self.statcounter = statcounter
        self.app = app
        self.screen = app.screen
        self.logo_image = logo_image
        self.cursor_image = cursor_image

    def render_bordered_to(self, screen, font, text, pos,
                           fg_color=(255, 255, 255), bg_color=(0, 0, 0),
                           aa=True, grow_by=1):
        bg_surf = font.render(text, aa, bg_color)
        fg_surf = font.render(text, aa, fg_color)
        pos = (pos[0]+grow_by, pos[1]+grow_by)
        screen.blit(bg_surf, (pos[0]-grow_by, pos[1]-grow_by))
        screen.blit(bg_surf, (pos[0]+grow_by, pos[1]-grow_by))
        screen.blit(bg_surf, (pos[0]-grow_by, pos[1]+grow_by))
        screen.blit(bg_surf, (pos[0]+grow_by, pos[1]+grow_by))
        screen.blit(fg_surf, pos)
        rect = fg_surf.get_rect().copy()
        rect.inflate_ip(grow_by, grow_by)
        rect.topleft = pos
        return rect

    def show_dialog(self, menu_strings, cursor_spin=0.0):
        ret = True
        self.clear_screen()
        pygame.display.flip()
        pygame.mouse.set_visible(True)  # TODO: only after first time
        pygame.event.set_grab(False)  # TODO: only after first time

        menu = Menu(menu_strings, self)
        menu.cursor_spin = cursor_spin
        selection = None
        while not self.get_bool('exit'):
            self.clear_screen()
            events = pygame.event.get()
            selection = self.draw_dialog(events, menu)
            if selection is not None:
                if selection == "BACK":
                    menu.draw_menu_buttons(menu_strings, None)
                    break
                if selection == "PLAY":
                    break
                if selection == "RESUME":
                    break
                if selection == "RETRY":
                    break
                if selection == "ABOUT":
                    menu.draw_menu_buttons(['BACK'], selection)
                if selection == "HELP":
                    menu.draw_menu_buttons(['BACK'], selection)
                if selection == "EXIT":
                    self.set_bool('exit', True)
                    ret = False
                    break
                    # fall through to on_exit handler
            else:
                menu.draw_menu_buttons(None, None, change_page=False)
            menu.draw_cursor(self.screen)
            # print("menu.select_i: " + str(menu.select_i))
            # print("menu.delay_count: " + str(menu.delay_count))
            pygame.display.update()  # dirty rect update
            pygame.display.flip()
            self.app.clock.tick(self.app.get_fps())
        self.clear_screen()
        # print("returning from menu")
        pygame.display.flip()
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(not self.get_bool('exit'))
        return ret

    def get_bool(self, name):
        return self._vars.get(name)

    def set_bool(self, name, v):
        self._vars[name] = v is True

    def draw_dialog(self, events, menu):
        selection = None
        self.app.check_music()
        pygame.event.pump()  # redraw Window so OS knows not frozen
        for event in events:
            if event.type == pygame.QUIT:
                self.set_bool('exit', True)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    selection = "BACK"
                if event.key == pygame.K_ESCAPE:
                    selection = "BACK"
                if event.key == pygame.K_UP:
                    menu.change_selection_up(self.screen)
                if event.key == pygame.K_DOWN:
                    menu.change_selection_down(self.screen)
                if event.key == pygame.K_RETURN:
                    selection = menu.get_selection()
            elif event.type == pygame.MOUSEMOTION:
                menu.change_selection_pos(event.pos, self.screen)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                menu.change_selection_pos(event.pos, self.screen)
                selection = menu.get_selection()
            elif event.type == pygame.USEREVENT:
                if event.code == pygame.USEREVENT_DROPFILE:
                    print("Tried to open file on MacOS (this should" +
                          " never happen:")
                    print("  " + str(event))
                else:  # should be event.code 0
                    self.app.continue_music()
                    print("music queue ended in menu:")
                    if event.code != 0:
                        print("unknown USEREVENT event.code: " +
                              str(event.code))

        return selection
    # endregion the menu functions

    def clear_screen(self):
        self.screen.fill(self.bg_color)
        # pygame.display.flip()
