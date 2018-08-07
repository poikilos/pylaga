#!/usr/bin/env python
"""stage manager for pylaga

Loads and provides the data for all stages of the game.
Mutates when next_stage is called.
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


class Stage:
    def __init__(self, enemymanager, playermanager):
        self.enemymanager = enemymanager
        self.playermanager = playermanager

        self.stages = [
            {
                'x_e_count':4, 'y_e_count':1, 'e':'eship', 'e_h':1,
                'music':'stage1.ogg'
            },
            {
                'x_e_count':5, 'y_e_count':2, 'e':'eship', 'e_h':1,
                'music':'stage2.ogg'
            },
            {
                'x_e_count':5, 'y_e_count':3, 'e':'eship', 'e_h':1,
                'music':'stage3.ogg'
            },
            {
                'x_e_count':6, 'y_e_count':1, 'e':'cship', 'e_h':4,
                'music':'stage4.ogg'
            },
            {
                'x_e_count':1, 'y_e_count':1, 'e':'bship', 'e_h':30,
                'music':'stage5.ogg'
            }
        ]
        self.hax = False
        if self.hax:
            self.stages = [
                {
                    'x_e_count':1, 'y_e_count':1, 'e':'cship', 'e_h':1,
                    'music':'stage5.ogg'
                },
                {
                    'x_e_count':1, 'y_e_count':1, 'e':'bship', 'e_h':1,
                    'music':'stage5.ogg'
                }
            ]
        self.current_i = 0

    def add_stage(self, x, y):
        self.stages.append({'x_e_count':x, 'y_e_count':y})

    def is_last_stage(self):
        return (self.current_i + 1) >= len(self.stages)

    def next_stage(self):
        if not self.is_last_stage():
            self.current_i += 1
        self.enemymanager.current_transition = 0

    def set_stage_number(self, stage):
        self.current_i = stage

    def get_data(self):
        if self.current_i < len(self.stages):
            return self.stages[self.current_i]
        else:
            msg = ("ERROR in Stage get_data: stage index " +
                   str(self.current_i) + " is out of range")
            print(msg)
            return {'ERROR':msg}
