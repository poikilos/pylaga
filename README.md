# Pylaga-py3
Pylaga-py3 is a simple remake of a classic game with a similar name, with some differences in gameplay, written with the pygame libs. Pylaga-py3 is a fork of Pylaga that works on Python 3 (including Kivy 1.8.0 for Python 3).
![Pylaga screenshot](https://github.com/poikilos/pylaga/raw/master/screenshot.jpg)

## Authors
* Music by MixMystery
* Forked (Python 3 and new graphics, particles, no globalvars, unified Entity class, sound [own work]) by: poikilos
* Previously forked (pylaga [python 2]) by: RJ Marsan (gmail RJMarsan)
* Original Creator: Derek Mcdonald
* CRYSTAL-Regular.ttf: Felipe Munoz (CC-BY SA 4.0 International)
* FreeSansBold.ttf: Copyleft 2002, 2003, 2005, 2008, 2009, 2010 Free Software Foundation ([GPL License](https://www.gnu.org/licenses/gpl-3.0.en.html))

## License
### Code
"LICENSE" file applies to code.
### Media
"CC-BY-SA 4.0 International.txt" file applies to media.

## How to install:

### Ubuntu/Debian:
```bash
sudo apt-get install python3 python3-pygame
python3 main.py
````

### Other Linux:
* Install python and pygame (python 3, which is default on some distros such as Ubuntu)
* `python3 main.py`

### Windows:
* Install python 3 (custom install, then in the list of options to install,
  look for "add Python to system PATH" then click on that drop-down box and choose "run from hard drive")
* Install pygame for python 3 (64-bit, unless you installed Python3 32-bit)
* doubleclick main.py

(this list of changes are only in poikilos fork)
## Changes
### (2018-08-05)
* added music and one sound
* created unified widget class for adding whatever you want wherever you want to the hud, and now Hud is a subclass of sprite.Group (widget class is Blip, and replaces StatCounter and HealthBar)
### (2018-08-05)
* combine Enemy, PlayerUnit, Bullet, EnemyBullet into one class
* add particles
* add empty.png so that sprite in spritegroup will be updated but not
  drawn.
* added multiple types of enemies
* added winning screen
### (2018-08-03)
* conform to PEP8
* rename almost all variables and classes with consistent naming convention
* fix unused but broken add_health method (used undefined local points instead of health param--so changed both to amount)
* eliminated globalvars.x, globalvars.y (analogous to p_unit.get_pos() aka p_unit.rect.topleft)
* renamed eliminated old screen variable and renamed surface to screen as per pygame usual convention
* eliminate globalvars WIN_RESX and WIN_RESY in favor of pygame display variables such as `w, h = pygame.display.get_surface().get_size()`
* eliminate globalvars ymin, ymax, xmin, xmax in favor of world_rect
* flip rects for in_range method so makes sense and doesn't require globals
* rename menulists to menus
* change set_pos to move_by to accurately describe what it does
* eliminate globalvars module
* eliminate mouse_is_anywhere in favor of get_selection that returns None if mouse over nothing (otherwise returns one of the menu strings now instead of a number)
* rename menu_action to draw_dialog
* combine init_menu, exit_menu, pause_menu into show_dialog
### (2015-03-03)
* (world.py) stopped using list of dirty rects (so-called "enemylist") that were erased before frame and were obtained by way of using draw method of sprite.RenderUpdates which is now replaced by sprite.Group which does not return dirty rects (to allow per-pixel alpha to be seen)--instead, clear whole screen then draw everything.
### (2015-03-01)
* improved player ship graphics with alpha
### (2015-03-03)
* (globalvars.py) change convert to convert_alpha so loaded images retain alpha channel
### (2015-02-24)
* (globalvars.py) prepended directory containing __file__ (py file) to DATADIR (such as to allow executing within Kivy)
* (all files) Make comment capitalization and style match galamax-py3 for to make diff output more clear
* (world.py) remove unecessary comments
* (all files) change indents to 4 spaces, and trim trailing spaces
* (world.py) show actual import exception
* ran 2to3.py
* (globalvars.py) Changed Move class to not require enum (not inherit from Enum) so that game works under Python 3.3 such as Kivy 1.8.0
* (menu.py, menus.py) fixed inconsistent use of tabs and spaces in indentation
* cast division result to int before being used as index to prevent the following error:
```
  File "player.py", line 75, in update
    self.image=playership[self.temper/temper_delay]
TypeError: list indices must be integers, not float
```

### RJ Marsan's TO DO LIST:
* proper transitions

### RJ Marsan's CHANGES:
* Moved the game to an object [he called it `gamelolz`, then poikilos fork renamed it `world`]
* Made a game manager
* Added Keyboard support
* Changed name (Pylaga sounds cooler anyways)
