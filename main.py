#!/usr/bin/env python
"""This is the main Pylaga module

This module instantiates the App class which runs the game
utilizing other modules.
Its short and sweet but thats the point.
"""

__author__ = ("2007-02-20 Derek Mcdonald (original),"
              " 2007-04-1 RJ Marsan,"
              " 2018 poikilos (Jake Gustafson)")
__version__ = '0.2.1'
__all__ = []  # declarees names of public API symbols (`[]` for no API)

import pygame
import os
import sys
import math
import random
from pygame.locals import*
from bullet import Bullet, EnemyBullet
from background import BackgroundManager
from enemy import Enemy, Swarm
from player import PlayerUnit
from stage import Stage
from hud import *
from menu import Menu
from world import World
from menus import Menus

if not pygame.font:
    print('Warning, fonts disabled')


########################################################################
#
#
#    simple class to manage the entire game...it helps with organization
#
#
class App:
    def __init__(self, resolution):
        pygame.init()
        self.clock = pygame.time.Clock()
        data_sub_dir = "data"
        ced = os.path.dirname(__file__)  # current executable directory
        self.DATA_PATH = os.path.join(ced, data_sub_dir)
        self.screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption("Pylaga " + __version__)
        self.world = World(self, self.screen)
        logo_image = self.load_file("screen-intro.png")
        cursor_image = self.load_file('pship.png')
        about_string = '''
            PYLAGA

            License: GPL 3.0

            Forked (Python 3 and new graphics, no globalvars)
             by: poikilos

            Previously forked (pylaga [python 2])
             by: RJ Marsan (RJMarsan@gmail.com)

            Original Creator:
             Derek Mcdonald

            CRYSTAL-Regular.ttf:
             Felipe Munoz (CC-BY SA 4.0 International)

            FreeSansBold.ttf:
             Copyleft 2002, 2003, 2005, 2008, 2009, 2010
             Free Software Foundation ([GPL License]
             (https://www.gnu.org/licenses/gpl-3.0.en.html))
        '''
        help_string = '''
            MOVE: move mouse
            FIRE: click/tap
            MENU: Esc
            MENU controls: mouse or arrows and enter key
                           (Esc or q key to resume/retry)
            EXIT: choose Exit from menu by clicking
                  or selecting then pressing enter
        '''
        pages_dict = {}
        pages_dict['ABOUT'] = {}
        pages_dict['ABOUT']['scroll_text'] = about_string
        pages_dict['HELP'] = {}
        pages_dict['HELP']['scroll_text'] = help_string
        self.menus = Menus(self.world.statcounter, self, logo_image,
                           cursor_image, pages_dict)
        init_menu_strings = ("PLAY", "ABOUT", "HELP", "EXIT")
        self.menus.show_dialog(init_menu_strings)
        print("starting world...")
        self.world.start(self.menus)
        tries = 1
        retry_menu_strings = ("RETRY", "ABOUT", "HELP", "EXIT",
                             "Score: %s" %
                             world.statcounter.get_points()
        )
        while ((not self.menus.get_bool('exit')) and
               (self.menus.show_dialog(retry_menu_strings,
                                       cursor_spin=-1.0))):
            print("starting world (tries: " + str(tries) + ")...")
            self.world.start(self.menus)
            tries += 1
        self.world.on_exit()

    def get_fps(self):
        return 60

    # general exception handler
    # (formerly used during imports to avoid exit without warning)
    # call this in any except clause
    def exception_handler():
        import traceback
        import sys
        type, info, trace = sys.exc_info()
        tracetop = traceback.extract_tb(trace)[-1]
        tracetext = 'File %s, Line %d' % tracetop[:2]
        if tracetop[2] != '?':
            tracetext += ', Function %s' % tracetop[2]
        exception_message = '%s:\n%s\n\n%s\n"%s"'
        message = (exception_message %
                   (str(type), str(info), tracetext, tracetop[3]))
        if type not in (KeyboardInterrupt, SystemExit):
            print(message)
        raise

    def load_file(self, filename):
        try:
            path = os.path.join(self.DATA_PATH, filename)
            return pygame.image.load(path).convert_alpha()
        except:
            print("Failed to load file "+filename)
        return None


# the one line that starts the game
# if __name__ == "__main__":
app = App((800,600))
