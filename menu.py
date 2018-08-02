#2007-04-1 RJ Marsan
#Pylaga
#Original: 2007-02-20 Derek Mcdonald
#Subclass of pylaga.py
#################################################################################################################
#
#	The Menu.
#
#       Its a generic menu object, it takes 1 parameter, and thats an array of strings to display
#
#
#import pygame os and sys libraries
import pygame, os, sys, math, random
import globalvars
from globalvars import WIN_RESX
from globalvars import WIN_RESY

##takes a tuple of menuitem strings as input
#a generic menu class
#very effective
class Menu:
    font_rect_height = None
    shipselectorsize = 50, 50 #updated before use
    
    def __init__(self, menuitems):
        self.font_size=20 #these do fairly obvious things
        self.offset_x=100
        self.offset_y=200
        self.spacing=10
        self.selection=0
        self.font = pygame.font.Font(globalvars.defaultfont,self.font_size)
        self.menuimgs=[]
        self.menurects=[]
        x=0
        for menuitem in menuitems:    #render all the strings that were inputted
            menuimg=self.font.render(menuitem, 1, globalvars.menucolor)
            menurect=menuimg.get_rect()
            if len(self.menuimgs)<1: #if not self.menuimgs:
                self.font_rect_height = menurect.height
                self.update_selector_size()
                self.spacing = int(WIN_RESY / 60)
                self.offset_x = (WIN_RESX - menurect.width) / 2
                self.offset_y = int(WIN_RESY / 2 + self.shipselectorsize[1] + self.spacing)
                menurect.move_ip(self.offset_x,self.offset_y)
            else:
                menurect.move_ip(self.offset_x,self.menurects[x-1].bottom+self.spacing)
            self.menuimgs.append(menuimg)
            self.menurects.append(menurect)
            x+=1

        self.menurect=pygame.Rect(self.menurects[0].topleft,self.menurects[len(self.menurects)-1].bottomright)
        self.selectedrect=pygame.Rect(self.menurect.left-self.shipselectorsize[0]-self.spacing,self.menurect.top,self.shipselectorsize[0],self.menurect.height)
        self.selectedimg=pygame.Surface(self.selectedrect.size)
        self.shipimg=pygame.transform.rotate(globalvars.playership[0],0)  #-90)
        self.shipimg=pygame.transform.scale(globalvars.playership[0], (self.shipselectorsize[0], self.shipselectorsize[1]))
        self.move=self.menurects[0].height+self.spacing
        self.selectedimg.blit(self.shipimg,pygame.Rect(0,self.selection*self.move,self.shipselectorsize[0],self.shipselectorsize[1]))
        x=0
        globalvars.surface.blit(globalvars.logo,globalvars.logo.get_rect())
        for menuimg in self.menuimgs:   #draw all the images to the display
            globalvars.surface.blit(menuimg,self.menurects[x])
            x+=1
        globalvars.surface.blit(self.selectedimg,self.selectedrect)
        pygame.display.flip()
        
    def update_selector_size(self):
        if self.font_rect_height is not None:
            self.shipselectorsize = int(self.font_rect_height), int(self.font_rect_height) #intentionally make a square using font height

    #generic selection changing class, not really used by outside
    #unless they know what they're doing
    def change_selection(self,selection):
        self.selectedimg.fill(globalvars.bgcolor)
        self.update_selector_size()
        self.selectedimg.blit(self.shipimg,pygame.Rect(0,selection*self.move,self.shipselectorsize[0],self.shipselectorsize[1]))
        globalvars.surface.blit(self.selectedimg,self.selectedrect)
        pygame.display.update(self.selectedrect)

     #simple methods to move selction up or down
    def change_selection_up(self):
        if self.selection >0:
            self.selection-=1
        self.change_selection(self.selection)

    def change_selection_down(self):
        if self.selection <len(self.menurects):
            self.selection+=1
        self.change_selection(self.selection)

    #a mouse oritened change_selection
    def change_selection_pos(self, pos):
        changed=False
        x=0
        for menuitem in self.menurects:
            if menuitem.collidepoint(pos):
                if self.selection!=x:
                    self.selection=x
                    changed=True
            x+=1
        if changed:
            self.change_selection(self.selection)

    #useful so that a random mouseclick doesnt do anything
    def mouse_is_anywhere(self,pos):
        for menuitem in self.menurects:
            if menuitem.collidepoint(pos):
                return True
        return False

    #returns selection (duh)
    def get_selection(self):
        return self.selection

#i'll do these later

    def disp_about(self):
        return

    def disp_help(self):
        return




