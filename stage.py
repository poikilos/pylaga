#!/usr/bin/env python
"""stage manager for pylaga

Needs lots of improvement
...thats never a good thing to hear
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


class Stage:
    enemy_stages = [(5, 2), (6, 3), (7, 4), (8, 4), (9, 4)]
    current_stage = 0

    def __init__(self, enemymanager, playermanager):
        self.enemymanager = enemymanager
        self.playermanager = playermanager

    def add_stage(self, x, y):
        self.enemy_stages.append((x, y))

    def next_stage(self):
        if len(self.enemy_stages) > self.current_stage + 1:
            self.current_stage += 1
        if globalvars.enemy_bullet_odds > 15:
            globalvars.enemy_bullet_odds -= 15
        self.enemymanager.current_transition = 0

    def set_stage(self, stage):
        self.current_stage = stage

    def get_stage(self):
        return self.enemy_stages[self.current_stage]
