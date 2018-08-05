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
from background import BackgroundManager
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
        # pygame.mixer.init(frequency=44100, size=-16, channels=2,
                          # buffer=4096)
        pygame.mixer.init(frequency=44100, channels=2)
        self.clock = pygame.time.Clock()
        data_sub_dir = "data"
        ced = os.path.dirname(__file__)  # current executable directory
        self.DATA_PATH = os.path.join(ced, data_sub_dir)
        self.screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption("Pylaga " + __version__)
        self.world = World(self, self.screen)
        logo_image = self.load_file("screen-intro.png")
        cursor_image = self.load_file('pship0.png')
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
            MENU: Escape ("Esc") key
              MENU controls: click/tap a choice, or use arrows and enter key
                                          (Esc or q key to resume/retry)
            EXIT: In the menu, click EXIT
                      (or select EXIT with arrows then press Enter key)
        '''
        pages_dict = {
            'ABOUT': {
                'scroll_text': about_string
            },
            'HELP': {
                'scroll_text': help_string
            }
        }
        # pages_dict['ABOUT']['scroll_text'] = about_string
        # pages_dict['HELP'] = {}
        # pages_dict['HELP']['scroll_text'] = help_string
        self.menus = Menus(self.world.statcounter, self, logo_image,
                           cursor_image, pages_dict)
        init_menu_strings = ("PLAY", "ABOUT", "HELP", "EXIT")
        self.menus.show_dialog(init_menu_strings)
        print("starting world...")
        self.world.start(self.menus)
        tries = 1
        retry_menu_strings = ["RETRY", "ABOUT", "HELP", "EXIT",
                             "Score: %s" %
                             self.world.statcounter.get_points()
        ]
        if self.world.won:
            retry_menu_strings.insert(0, self.world.won_msg)
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

    def zero_padded(self, i, min_digits):
        s = str(i)
        if len(s) < min_digits:
            s = '0'*(min_digits-len(s)) + s
        return s

    def get_seq_info(self, name_except_number, dot_ext=".png"):
        results = {'min_digits':None, 'first_i':None, 'directory':None,
                   'tried_paths':[], 'found':False}
        try_dirs = [
            '.',
            self.DATA_PATH,
            os.path.dirname(os.path.abspath(__file__))
        ]
        no_pad_is_this_length = 6
        for parent in try_dirs:
            for min_digits in range(no_pad_is_this_length):
                for first_i in range(2):
                    name = (name_except_number +
                            self.zero_padded(first_i, min_digits) +
                            dot_ext)
                    path = os.path.join(parent, name)
                    if os.path.isfile(path):
                        results['min_digits'] = min_digits
                        results['first_i'] = first_i
                        results['directory'] = parent
                        results['found'] = True
                        return results
                    else:
                        results['tried_paths'].append(path)
        return results


    def load_seq(self, name_except_number, dot_ext=".png",
                 min_digits=0):
        results = None
        info = self.get_seq_info(name_except_number)
        if info['found']:
            results = []
            i = info['first_i']
            while True:
                name = (name_except_number +
                        self.zero_padded(i, info['min_digits']) +
                        dot_ext)
                path = os.path.join(info['directory'], name)
                if os.path.exists(path):
                    surf = self.load_file(name,
                                          try_dirs=[info['directory']])
                    if surf is not None:
                        results.append(surf)
                        i += 1
                    else:
                        print("ERROR in load_seq: image unreadable: " +
                              path)
                        break
                else:
                    break  # no errors, just no more images left in seq
        else:
            print("No png sequence found named " + name_except_number +
                  ". Tried:")
            for try_path in results['tried_paths']:
                print("  " + try_path)
        return results


    def load_file(self, name, repress_error_enable=False,
                  try_dirs=None, file_type='image'):
        try:
            if try_dirs is None:
                try_dirs = [
                    '.',
                    self.DATA_PATH,
                    os.path.dirname(os.path.abspath(__file__))
                ]
            for parent in try_dirs:
                path = os.path.join(parent, name)
                if os.path.isfile(path):
                    if file_type == 'image':
                        return pygame.image.load(path).convert_alpha()
                    else:
                        return pygame.mixer.Sound(path)
        except:
            if not repress_error_enable:
                print("Failed to load file "+name)
        return None


# the one line that starts the game
# if __name__ == "__main__":
app = App((800,600))
