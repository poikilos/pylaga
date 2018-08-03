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
import globalvars
from bullet import Bullet, EnemyBullet
from background import BackgroundManager, bgstars
from enemy import Enemy, EnemyManager
from player import Player
from stage import Stage
from display import *
from menu import Menu
from world import World
from menulists import MenuLists

if not pygame.font:
    print('Warning, fonts disabled')


########################################################################
#
#
#    simple class to manage the entire game...it helps with organization
#
#
class App:
    def __init__(self):
        self.world = World(self)
        self.menus = MenuLists()
        self.menus.init_menu()
        self.world.start(self.menus)
        pygame.display.set_caption("Pylaga " + __version__)
        while ((not self.menus.get_bool('exit')) and
               (self.menus.exit_menu())):
            self.world.start(self.menus)
        self.world.on_exit()

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


# the one line that starts the game
# if __name__ == "__main__":
app = App()
