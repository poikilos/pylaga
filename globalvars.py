"""global variables for pylaga

define global variables
wow i really dont know what most of these do anymore
"""
__author__ = ("2007-02-20 Derek Mcdonald (original),"
              " 2007-04-1 RJ Marsan,"
              " 2018 poikilos (Jake Gustafson)")
__version__ = '0.2.1'
__all__ = []

import os
import sys
import math
import random

# TODO: deprecate globals

global FPS
FPS = 60
global REFRESH_TIME
REFRESH_TIME = FPS*3

# enemy's inital speed
global init_enemy_speed
init_enemy_speed = 3
# decided its best to make it an object
# distance between enemys
global enemy_spacing_x, enemy_spacing_y, enemy_bullet_odds
enemy_spacing_x = 15
enemy_spacing_y = 10
enemy_bullet_odds = 15
# size of the bitmap...  GET RID OF THESE
global enemy_width, enemy_height
enemy_width = 30
enemy_height = 30
# some random vars
global explosion_speed
explosion_speed = 5
# vars to determine where the score is
global points_x, points_y, health_x, health_y, points_text_size
global max_health
global healthbar_offset_y, healthbar_offset_x, healthbar_width
points_x = 0
points_y = 5
health_x = 0
health_y = 50
healthbar_offset_y = 60
healthbar_offset_x = 10
healthbar_width = 7
points_text_size = 14
max_health = 100
# vars for the bg star_rects
global BG_Speed, init_stars, star_color
BG_Speed = 5
init_stars = 15
star_color = (150, 150, 150)

# color vars
global bg_color, hud_color
bg_color = (0, 0, 0)
hud_color = (128, 128, 128)
menu_color = (195, 227, 247)

# started out random, now is an important part, its the frames that have
# gone by helps so not everything is rendered every frame
global asdf
asdf = 0

# default font
default_font = "freesansbold.ttf"


# print("Global Variables Loaded")
