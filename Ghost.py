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
import random

class Ghost:
    def __init__(self,mapa, mc, x_mc, y_mc, xini, yini, dir, tipo):
        #Matriz de control que almacena los IDs de las intersecciones
        self.MC = mc
        #Vectores que almacenan las coordenadas 
        self.XPxToMC = x_mc
        self.YPxToMC = y_mc
        #se resplanda el mapa en terminos de pixeles
        self.mapa = mapa
        
        # Posición inicial del fantasma (en píxeles, igual que Pacman)
        self.x = xini
        self.y = yini
 
        self.dir = dir      # dirección actual
        self.tipo = tipo    # para distinguir entre fantasmas (1,2,3,4)
 
        self.MAX_X = mapa.shape[1] - 1  # 358
        self.MAX_Y = mapa.shape[0] - 1  # 360
        
        # Listas índice MC -> píxel real
        self.xMC_px = [0, 30, 71, 114, 156, 199, 242, 286, 328, 358]
        self.yMC_px = [0, 51, 90, 130, 168, 208, 244, 282, 320, 360]

        
    def loadTextures(self, texturas, id):
        self.texturas = texturas
        self.Id = id

    
    def sigue_adelante(self):
        #print(f"Fantasma en: {self.x}, {self.y} - Pared: {self.mapa[int(self.y)][int(self.x)]}")
        if self.dir == 1 and self.x + 1 <= self.MAX_X and self.mapa[self.y][self.x + 1] == 1:
            self.x += 1
        elif self.dir == 3 and self.x - 1 >= 0 and self.mapa[self.y][self.x - 1] == 1:
            self.x -= 1
        elif self.dir == 2 and self.y + 1 <= self.MAX_Y and self.mapa[self.y + 1][self.x] == 1:
            self.y += 1
        elif self.dir == 4 and self.y - 1 >= 0 and self.mapa[self.y - 1][self.x] == 1:
            self.y -= 1
        else:
            # Hay pared, elegir dirección aleatoria válida
            opciones = []
            if self.x + 1 <= self.MAX_X and self.mapa[self.y][self.x + 1] == 1: opciones.append(1)
            if self.x - 1 >= 0          and self.mapa[self.y][self.x - 1] == 1: opciones.append(3)
            if self.y + 1 <= self.MAX_Y and self.mapa[self.y + 1][self.x] == 1: opciones.append(2)
            if self.y - 1 >= 0          and self.mapa[self.y - 1][self.x] == 1: opciones.append(4)
            if opciones:
                self.dir = random.choice(opciones)
                self.sigue_adelante()
 

    def interseccion_random(self, pacmanXY):
        px, py = pacmanXY
        # Intentar la dirección que más acerque al Pacman
        preferidas = []
        if px > self.x: preferidas.append(1)
        if px < self.x: preferidas.append(3)
        if py > self.y: preferidas.append(2)
        if py < self.y: preferidas.append(4)
 
        for d in preferidas:
            puede = False
            if d == 1 and self.x + 1 <= self.MAX_X and self.mapa[self.y][self.x + 1] == 1: puede = True
            if d == 3 and self.x - 1 >= 0          and self.mapa[self.y][self.x - 1] == 1: puede = True
            if d == 2 and self.y + 1 <= self.MAX_Y and self.mapa[self.y + 1][self.x] == 1: puede = True
            if d == 4 and self.y - 1 >= 0          and self.mapa[self.y - 1][self.x] == 1: puede = True
            if puede:
                self.dir = d
                return
 
        # Si ninguna preferida funciona, dirección aleatoria
        opciones = []
        if self.x + 1 <= self.MAX_X and self.mapa[self.y][self.x + 1] == 1: opciones.append(1)
        if self.x - 1 >= 0          and self.mapa[self.y][self.x - 1] == 1: opciones.append(3)
        if self.y + 1 <= self.MAX_Y and self.mapa[self.y + 1][self.x] == 1: opciones.append(2)
        if self.y - 1 >= 0          and self.mapa[self.y - 1][self.x] == 1: opciones.append(4)
        if opciones:
            self.dir = random.choice(opciones)
            
    def interseccion_solo_random(self, pacmanXY):
        px, py = pacmanXY
 
        # Si ninguna preferida funciona, dirección aleatoria
        opciones = []
        if self.x + 1 <= self.MAX_X and self.mapa[self.y][self.x + 1] == 1: opciones.append(1)
        if self.x - 1 >= 0          and self.mapa[self.y][self.x - 1] == 1: opciones.append(3)
        if self.y + 1 <= self.MAX_Y and self.mapa[self.y + 1][self.x] == 1: opciones.append(2)
        if self.y - 1 >= 0          and self.mapa[self.y - 1][self.x] == 1: opciones.append(4)
        if opciones:
            self.dir = random.choice(opciones)
            
    def interseccion_inteligente(self, pacmanXY):
        px, py = pacmanXY
        direcciones = [1,2,3,4]
    
    def update2(self,pacmanXY):     
        if self.XPxToMC[self.x] != -1 and self.YPxToMC[self.y] != -1:
            self.interseccion_solo_random(pacmanXY)
        self.sigue_adelante()
    
    def update1(self,pacmanXY):     
        if self.XPxToMC[self.x] != -1 and self.YPxToMC[self.y] != -1:
            self.interseccion_random(pacmanXY)
        self.sigue_adelante()
    
    def draw(self):
        
        DimBoard = 20
        offset = 10
        glColor3f(1.0,1.0,1.0) #para ver los colores originsles tiene que estar en blnaco
        glEnable(GL_TEXTURE_2D)
        #front face
        glBindTexture(GL_TEXTURE_2D, self.texturas[self.Id])    
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
         
 