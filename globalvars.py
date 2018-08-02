# 2007-04-1 RJ Marsan
# Pylaga
# Original: 2007-02-20 Derek Mcdonald
# Subclass of pylaga.py
###############################################################################
#
#
# TODO: remove globals
# ALLLLLLLLLLLLLLLLLLLLLLLLLLLLL the variables (or LITERALS) in this
# entire game
# Everything that does not change, or starts at a certain value, SHOULD
# be here however, it has been decided that this should be majorly cut
# down.
# so...... DIE
#
###############################################################################
import pygame
import os
import sys
import math
import random

# define global variables
# wow i really dont know what most of these do anymore
# TODO: clean this up
global VERSION
VERSION = "Pylaga .11"
global DATADIR
DATADIR = "data/"

ced = os.path.dirname(__file__)  # current executable directory
DATADIR = os.path.join(ced, DATADIR)

global FPS
FPS = 60
global WIN_RESX
WIN_RESX = 800
global WIN_RESY
WIN_RESY = 600
global REFRESH_TIME
REFRESH_TIME = FPS*3

global left_boarder
left_boarder = 50
global right_boarder
right_boarder = 50

global gamewindow
gamewindow = pygame.Rect(left_boarder, 0, WIN_RESX-right_boarder, WIN_RESY)

global ymin, ymax, xmin, xmax
ymin = 0
ymax = WIN_RESY
xmax = WIN_RESX-right_boarder
xmin = left_boarder

# yay arrays! they make the world go round, and iderate.
# basically all the objects in the game reside in their own special
# array and then all one needs to do is go through these arrays and
# call functions and stuff. it makes sense in here *points to brain*
global player_list, side_panel
player_list = pygame.sprite.Group()
side_panel = pygame.sprite.Group()
# bullet's initial speed 'n shape
global BULLET_SPEED, BULLET_WIDTH
BULLET_SPEED = 10
BULLET_WIDTH = 10
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
global smooth_scroll_var1, smooth_scroll_var2, explosion_speed
smooth_scroll_var1 = 10
smooth_scroll_var2 = 2
explosion_speed = 5
# vars to determine where the score is
global points_x, points_y, health_x, health_y, points_text_size, max_health
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
# vars for the bg stars
global BG_Speed, init_stars, star_color
BG_Speed = 5
init_stars = 15
star_color = (150, 150, 150)

# color vars
global bgcolor, sidepanelcolor
bgcolor = (0, 0, 0)
sidepanelcolor = (128, 128, 128)
menucolor = (195, 227, 247)

# started out random, now is an important part, its the frames that have
# gone by helps so not everything is rendered every frame
global asdf
asdf = 0

# the clock for keeping movement in time
global clock
clock = pygame.time.Clock()

# default font
defaultfont = "freesansbold.ttf"

# create window and set up background image
window = pygame.display.set_mode((WIN_RESX, WIN_RESY))
pygame.display.set_caption(VERSION)
surface = pygame.display.get_surface()


def load_file(filename):
    try:
        imgfile = os.path.join(filename)
        return pygame.image.load(imgfile).convert_alpha()
    except:
        print("Failed to load file "+filename)


# loads the background file
screen = pygame.Surface((WIN_RESX, WIN_RESY))
screen.fill(bgcolor)

# loads logo
logo = load_file(DATADIR+"screen-intro.png")

# array to hold some more animations
global playership
playership = []
# loads playership image
playership.append(load_file(DATADIR+'pship.png'))
playership.append(load_file(DATADIR+'pship1.png'))
playership.append(load_file(DATADIR+'pship2.png'))
playership.append(load_file(DATADIR+'pship3.png'))

# loads enemy ship image
enemyship = (load_file(DATADIR+'eship.png'))

# loads laser, laser1 and all other images associated with pshoot
shot = load_file(DATADIR+'laser.png')
eshot = load_file(DATADIR+'elaser.bmp')

# array to hold the explosions
global explosions
explosions = []
# load the collision animations... dont ask why so many just lazy
explosions.append(load_file(DATADIR+'explosion1.bmp'))
explosions.append(load_file(DATADIR+'explosion2.bmp'))
explosions.append(load_file(DATADIR+'explosion3.bmp'))
explosions.append(load_file(DATADIR+'explosion4.bmp'))
explosions.append(load_file(DATADIR+'explosion5.bmp'))

# initialize pygame
pygame.init()

# print("Global Variables Loaded")
