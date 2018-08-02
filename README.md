# Pylaga-py3
Pylaga-py3 is a simple remake of a classic game with a similar name, with some differences in gameplay, written with the pygame libs. Pylaga-py3 is a fork of Pylaga that works on Python 3 (including Kivy 1.8.0 for Python 3).

## Authors
Forked (Python 3 and new graphics) by: poikilos
Previously forked (pylaga [python 2]) by: RJ Marsan (RJMarsan@gmail.com)
Original Creator: Derek Mcdonald
CRYSTAL-Regular.ttf: Felipe Munoz (CC-BY SA 4.0 International)
FreeSansBold.ttf: Copyleft 2002, 2003, 2005, 2008, 2009, 2010 Free Software Foundation ([GPL License](https://www.gnu.org/licenses/gpl-3.0.en.html))

## How to install: 

### Ubuntu/Debian:
sudo apt-get install python3 python3-pygame
Run ./main.py

### Other Linux:
Install python and pygame (python 3, which is default on some distros such as Ubuntu)
python pylaga.py

### Windows:
Install python 3
Install pygame for python 3
doubleclick main.py

## Changes (Pylaga-py3):
*(2015-03-03)-game.py: stopped using list of dirty rects (so-called "enemylist") that were erased before frame and were obtained by way of using draw method of sprite.RenderUpdates which is now replaced by sprite.Group which does not return dirty rects (to allow per-pixel alpha to be seen)--instead, clear whole screen then draw everything.
*(2015-03-01)-improved player ship graphics with alpha
*(2015-03-03)-globalvars.py: change convert to convert_alpha so loaded images retain alpha channel
*(2015-02-24)-globalvars.py: prepended directory containing __file__ (py file) to DATADIR (such as to allow executing within Kivy)
*(2015-02-24)all files: Make comment capitalization and style match galamax-py3 for to make diff output more clear
*(2015-02-24)game.py: removed unecessary comments
*(2015-02-24)all files: changed indents to 4 spaces, and trim trailing spaces
*(2015-02-24)-game.py: show actual import exception
*(2015-02-24)-ran 2to3.py
*(2015-02-24)-globalvars.py: Changed Move class to not require enum (not inherit from Enum) so that game works under Python 3.3 such as Kivy 1.8.0
*(2015-02-24)-menu.py, menulists.py: fixed inconsistent use of tabs and spaces in indentation
*(2015-02-24)-cast division result to int before being used as index to prevent the following error:
  File "player.py", line 75, in update
    self.image=playership[self.state/explosion_speed]
TypeError: list indices must be integers, not float

### Pylaga-py3 Known Issues:
(x or date = done)
* remove unusable branding (Galaga is a registered trademark of Atari(R))

### RJ Marsan's TO DO LIST:
* correct implementation of stage progression
* other misc. things to make the game look purrty
* proper transitions

### RJ Marsan's CHANGES:
* Moved the game to an object called 'gamelolz'
* Made a game manager
* Added Keyboard support
* Changed name (Pylaga sounds cooler anyways)
