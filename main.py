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

# Se carga el archivo de la clase Cubo
import sys
sys.path.append('..')
from Pacman import Pacman
from Ghost import Ghost
from Node import Node
import math

screen_width = 800
screen_height = 800

#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
#Dimension del plano
DimBoard = 400

#Arreglo para el manejo de texturas
textures = []
#Nombre de los archivos a usar
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
file_1 = os.path.join(BASE_PATH, 'mapa.bmp') #imagen vectorizada
img_pacman = os.path.join(BASE_PATH, 'pacman.bmp')
img_ghost1 = os.path.join(BASE_PATH, 'marianin.bmp')
img_ghost2 = os.path.join(BASE_PATH, 'lupis.bmp')
img_ghost3 = os.path.join(BASE_PATH, 'hope.bmp')
img_ghost4 = os.path.join(BASE_PATH, 'ale.bmp')
file_gameover = os.path.join(BASE_PATH, 'gameover.bmp')


file_csv = os.path.join(BASE_PATH, 'mapa.csv')
matrix = np.array(pd.io.parsers.read_csv(file_csv, header=None)).astype("int")

#Matriz de Control para mapeo entre pixeles <-> coord donde se localizan esquinas
MC = [
    [10,0,21,0,11,10,0,21,0,11],
    [24,0,25,21,23,23,21,25,0,22],
    [12,0,22,12,11,10,13,24,0,13],
    [0,0,0,10,23,23,11,0,0,0],
    [26,0,25,22,0,0,24,25,0,27],
    [0,0,0,24,0,0,22,0,0,0],
    [10,0,25,23,11,10,23,25,0,11],
    [12,11,24,21,23,23,21,22,10,13],
    [10,23,13,12,11,10,13,12,23,11],
    [12,0,0,0,23,23,0,0,0,13]
]

xMC = [0,30,71,114,156,199,242,286,328,358]

XPxToMC = np.full(359, -1, dtype=int)
XPxToMC[0] = 0
XPxToMC[30] = 1
XPxToMC[71] = 2
XPxToMC[114] = 3
XPxToMC[156] = 4
XPxToMC[199] = 5
XPxToMC[242] = 6
XPxToMC[286] = 7
XPxToMC[328] = 8
XPxToMC[358] = 9
 
yMC = [0,51,90,130,168,208,244,282,320,360]
#YPxToMC = np.zeros((361,), dtype=int)
YPxToMC = np.full(361, -1, dtype=int)
YPxToMC[0] = 0
YPxToMC[51] = 1
YPxToMC[90] = 2
YPxToMC[130] = 3
YPxToMC[168] = 4
YPxToMC[208] = 5
YPxToMC[244] = 6
YPxToMC[282] = 7
YPxToMC[320] = 8
YPxToMC[360] = 9

#pathfinding variables
path = []
grid = []

#pacman
pc = Pacman(matrix, MC, XPxToMC, YPxToMC)
#fantasmas
#ghosts = []
"""
ghosts = [
    # Esquina Superior Izquierda: xMC[0], yMC[0] -> (0, 0)
    Ghost(matrix, MC, XPxToMC, YPxToMC, xMC[0], yMC[0], 1, 1),
    
    # Esquina Superior Derecha: xMC[9], yMC[0] -> (358, 0)
    Ghost(matrix, MC, XPxToMC, YPxToMC, xMC[9], yMC[0], 3, 2),
    
    # Esquina Inferior Izquierda: xMC[0], yMC[9] -> (0, 360)
    Ghost(matrix, MC, XPxToMC, YPxToMC, xMC[0], yMC[9], 4, 3),
    
    # Esquina Inferior Derecha: xMC[9], yMC[9] -> (358, 360)
    Ghost(matrix, MC, XPxToMC, YPxToMC, xMC[9], yMC[9], 4, 4)
]"""
ghosts = [
    # Fantasma 1: Cooperativo A - Arriba de la caja
    Ghost(matrix, MC, XPxToMC, YPxToMC, xMC[4], yMC[3], 1, 1),
    
    # Fantasma 2: Cooperativo B - Arriba de la caja
    Ghost(matrix, MC, XPxToMC, YPxToMC, xMC[5], yMC[3], 3, 2),
    
    # Fantasma 3: Aleatorio - Abajo de la caja
    Ghost(matrix, MC, XPxToMC, YPxToMC, xMC[4], yMC[5], 4, 3),
    
    # Fantasma 4: Inteligente - Abajo de la caja
    Ghost(matrix, MC, XPxToMC, YPxToMC, xMC[5], yMC[5], 4, 4)
]

pygame.init()

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    #X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    glLineWidth(1.0)

def Texturas(filepath):
    textures.append(glGenTextures(1))
    id = len(textures) - 1
    glBindTexture(GL_TEXTURE_2D, textures[id])
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image = pygame.image.load(filepath).convert()
    w, h = image.get_rect().size
    image_data = pygame.image.tostring(image,"RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data) 
    glGenerateMipmap(GL_TEXTURE_2D) 
    
def Init():
    screen = pygame.display.set_mode(
        (400, 400), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: cubos")
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,400,400,0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0,0,0,0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    #textures[0]: plano
    Texturas(file_1)
    #textures[1]: pacman
    Texturas(img_pacman)
    #textures[2]: fantasma1
    Texturas(img_ghost1)
    #textures[3]: fantasma2
    Texturas(img_ghost2)
    #textures[4]: fantasma3
    Texturas(img_ghost3)
    #textures[5]: fantasma4
    Texturas(img_ghost4)
    #fin
    Texturas(file_gameover)
    #se pasan las texturas a los objetos
    pc.loadTextures(textures,1)

    for i in range(len(ghosts)):
        # La textura de los fantasmas empieza en el índice 2 de la lista 'textures'
        ghosts[i].loadTextures(textures, i + 2)
    
def PlanoTexturizado():
    #Activate textures
    glColor3f(1.0,1.0,1.0) #para ver los colores originsles tiene que estar en blnaco
    glEnable(GL_TEXTURE_2D)
    #front face
    glBindTexture(GL_TEXTURE_2D, textures[0])    
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex2d(0, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex2d(0, DimBoard)
    glTexCoord2f(1.0, 1.0)
    glVertex2d(DimBoard, DimBoard)
    glTexCoord2f(1.0, 0.0)
    glVertex2d(DimBoard, 0)
    glEnd()              
    glDisable(GL_TEXTURE_2D)

#MI BELLO A STAR
def a_star(g1, g2, pacmanXY):
   
    ALPHA = 0.7  # Importancia de acercarse al Pacman
    BETA = 0.3   # Importancia de separarse entre ellos
    
    #nodo inicial
    nodo_raiz = Node((g1.x, g1.y), (g2.x, g2.y), (g1.dir, g2.dir))
    open_list = [nodo_raiz]
    

    # profundidad 2 (Expandimos la raíz y sus hijos inmediatos)
    for _ in range(2):
        if not open_list: break
        
        open_list.sort(key=lambda n: n.f) # El más prometedor primero
        actual = open_list.pop(0)
        
        # Generar combinaciones de movimientos para ambos fantasmas
        for h1 in g1.children():
            for h2 in g2.children():
                nuevo = Node(h1['pos'], h2['pos'], (h1['dir'], h2['dir']), parent=actual)
                
                # --- EVALUACIÓN EUCLIDIANA ---
                # Distancia de los fantasmas al Pacman
                dist_p1 = math.sqrt((nuevo.f1_x - pacmanXY[0])**2 + (nuevo.f1_y - pacmanXY[1])**2)
                dist_p2 = math.sqrt((nuevo.f2_x - pacmanXY[0])**2 + (nuevo.f2_y - pacmanXY[1])**2)
                atraccion_pacman = (dist_p1 + dist_p2) / 2 # Promedio de cercanía
                
                # Distancia entre fantasmas (Queremos que sea GRANDE, por eso restamos)
                dist_entre_fantasmas = math.sqrt((nuevo.f1_x - nuevo.f2_x)**2 + (nuevo.f1_y - nuevo.f2_y)**2)
                # Penalizamos si están a menos de 100px
                repulsion = 100 - dist_entre_fantasmas if dist_entre_fantasmas < 100 else 0
                
                # --- FÓRMULA FINAL ---
                # g = pasos dados, h = (Alpha * Distancia) + (Beta * Penalización por estar juntos)
                nuevo.g = actual.g + 1
                nuevo.h = (ALPHA * atraccion_pacman) + (BETA * repulsion)
                nuevo.f = nuevo.g + nuevo.h
                
                open_list.append(nuevo)

    # 3. Retornar las direcciones del mejor nodo encontrado
    if open_list:
        open_list.sort(key=lambda n: n.f)
        return open_list[0].dirs
    
    return g1.dir, g2.dir

#MUERE :(
def verificar_colision():
    global game_over
    distancia_minima = 12 
    for g in ghosts:
        dist = math.sqrt((g.x - pc.x)**2 + (g.y - pc.y)**2)
        if dist < distancia_minima:
            if not game_over: # Para que el sonido solo suene una vez
                print("¡GAME OVER! Presiona ESPACIO para salir.")
                reproducir_muerte()
                game_over = True

def reproducir_muerte():
    # Carga y reproduce el sonido de muerte original
    # Asegúrate de tener el archivo 'death.wav' en tu carpeta
    pygame.mixer.init()
    try:
        sonido_muerte = pygame.mixer.Sound("death.wav")
        sonido_muerte.play()
    except:
        print("No se encontró el archivo de sonido")

def draw_game_over_box():
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[6]) # Usamos la nueva textura
    glColor3f(1.0, 1.0, 1.0) # Asegurar color original de la imagen
    
    # Definimos un cuadro pequeño centrado (ej. 200x100px)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex2f(100, 150)
    glTexCoord2f(0.0, 1.0); glVertex2f(100, 250)
    glTexCoord2f(1.0, 1.0); glVertex2f(300, 250)
    glTexCoord2f(1.0, 0.0); glVertex2f(300, 150)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
dir = 0
olddir = 0

def display():
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    PlanoTexturizado()
    band = 10
    global dir, olddir, game_over
    
    if not game_over:
        verificar_colision()
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]:
            dir = 1  
        if keys[pygame.K_DOWN]:
            dir = 2
        if keys[pygame.K_LEFT]:
            dir = 3
        if keys[pygame.K_UP]:
            dir = 4
    
        
        olddir = pc.update(olddir,dir)
        pc.draw()
     
        pacman_pos = [pc.x, pc.y]
        # Solo recalcular el camino A* cuando los fantasmas lleguen a una intersección real
        if (ghosts[0].XPxToMC[ghosts[0].x] != -1 and ghosts[0].YPxToMC[ghosts[0].y] != -1) or (ghosts[1].XPxToMC[ghosts[1].x] != -1 and ghosts[1].YPxToMC[ghosts[1].y] != -1):
    
            d1, d2 = a_star(ghosts[0], ghosts[1], pacman_pos)
            ghosts[0].dir = d1
            ghosts[1].dir = d2

        
        for g in (ghosts):
            g.draw()
            
            if g == ghosts[0] or g == ghosts[1]: #el azul y naranja son cooperativos
                # Estos son los cooperativos, ya tienen su 'dir' asignada por el A*
                # Solo necesitan seguir adelante
                g.sigue_adelante()
                
            elif g == ghosts[3]:
                # El fantasma 4, el rojo, sigue con su lógica inteligente individual
                g.update1(pacman_pos) 
            
            else:
                # El resto sigue con lógica aleatoria 3rosa random
                g.update2(pacman_pos)
            
    if game_over:
        draw_game_over_box()
    
done = False
game_over = False
Init()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            if game_over and event.key == pygame.K_SPACE:
                done = True
    
   
    
    display()
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
    

