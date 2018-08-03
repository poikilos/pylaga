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
        self.menus = Menus(self.world.statcounter, self, logo_image,
                           cursor_image)
        self.menus.init_menu()
        self.world.start(self.menus)
        while ((not self.menus.get_bool('exit')) and
               (self.menus.exit_menu())):
            self.world.start(self.menus)
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
