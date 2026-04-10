import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import os
import numpy as np
import pandas as pd


class Pacman:
    def __init__(self,mapa, mc, x_mc, y_mc):
        #Matriz de control que almacena los IDs de las intersecciones
        self.MC = mc
        #Vectores que almacenan las coordenadas 
        self.XPxToMC = x_mc
        self.YPxToMC = y_mc
        #se resplanda el mapa en terminos de pixeles
        self.mapa = mapa
        #si el pacman se encuentra en estado inicial del juego
        self.start = 1     
        #
        self.x = 0
        self.y = 0 
        self.currxp = 0
        self.currxy = 0 
    
        
        self.MAX_X = mapa.shape[1] - 1  # 358
        self.MAX_Y = mapa.shape[0] - 1  # 360
         
        
    def loadTextures(self, texturas, id):
        self.texturas = texturas
        self.Id = id
        
    def update(self,olddir, dir):
        #print(self.YPxToMC[self.y])
        #print(dir)
        #print(olddir)
        print(f"pacman en: {self.x}, {self.y} - Pared: {self.mapa[int(self.y)][int(self.x)]}")
        #print(dir == 1 and self.x + 1 <= self.MAX_X and self.mapa[self.y][self.x + 1] == 1)
        #print(self.XPxToMC[self.x]  != -1 and self.YPxToMC[self.y] != -1 )
        print(self.XPxToMC[self.x], self.YPxToMC[self.y] )
        
        
        if self.XPxToMC[self.x]  != -1 and self.YPxToMC[self.y] != -1 :
        #if self.XPxToMC[self.x] != -1 and self.YPxToMC[self.y] != -1:
        
            #if dir == 1 and  self.mapa[self.y][self.x +1] == 1: #derecha
            if   dir == 1 and self.x + 1 <= self.MAX_X and self.mapa[self.y][self.x + 1] == 1:  # derecha
                #print(self.x+2)
                #print(self.y)
                #print(self.mapa[self.x +2][self.y])
                self.x += 1
                #self.x = self.xMC_px[xi + 1]
                olddir = dir
                
            elif dir == 3 and self.x - 1 >= 0 and self.mapa[self.y][self.x -1] == 1 : #izquierda
                self.x -= 1
                olddir = dir
                
            elif dir == 2 and self.y + 1 <= self.MAX_Y and self.mapa[self.y + 1][self.x] == 1 : #abajo
                self.y += 1
                olddir = dir
            elif dir == 4 and self.y - 1 >= 0 and self.mapa[self.y -1][self.x ] == 1 : #arriba
                self.y -= 1 
                olddir = dir
            
                
        else:
           
            #dir = olddir
            if olddir == 1 and self.x + 1 <= self.MAX_X and self.mapa[self.y][self.x +1] == 1 : #derecha
                self.x += 1
            elif olddir == 3 and self.x - 1 >= 0 and self.mapa[self.y][self.x - 1] == 1 : #izquierda
                self.x -= 1
            elif olddir == 2 and self.y + 1 <= self.MAX_Y and self.mapa[self.y + 1][self.x] == 1 : #abajo
                self.y += 1
            elif olddir == 4 and self.y - 1 >= 0 and self.mapa[self.y -1][self.x ] == 1 : #arriba
                self.y -= 1 
        
        return olddir
    
    def draw(self):
        DimBoard = 20
        offset = 10
        glColor3f(1.0,1.0,1.0) #para ver los colores originsles tiene que estar en blnaco
        glEnable(GL_TEXTURE_2D)
        #front face
        glBindTexture(GL_TEXTURE_2D, self.texturas[1])    
        glBegin(GL_QUADS)
        glTexCoord2f(0.0,0.0)
        glVertex2d(self.x + offset, self.y + offset)
        glTexCoord2f(0.0, 0.0 + 1.0)
        glVertex2d(self.x + offset, self.y + DimBoard + offset)
        glTexCoord2f(0.0 + 1.0, 0.0 + 1.0)
        glVertex2d(self.x+DimBoard + offset, self.y + DimBoard + offset)
        glTexCoord2f(0.0+ 1.0, 0.0)
        glVertex2d(self.x+DimBoard + offset, self.y + offset)
        glEnd()              
        glDisable(GL_TEXTURE_2D)
         
    
  