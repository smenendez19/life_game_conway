# Imports

import time

import numpy as np
import pygame

# Inicio pygame
pygame.init()
pygame.display.set_caption("Juego de la Vida")

# Dimensiones de la ventana
width, height, width_max, height_max = 500, 500, 600, 600
screen = pygame.display.set_mode((height_max, width))

# Fondo
black = 25, 25, 25
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
screen.fill(black)

# Celdas
nxC, nyC = 50, 50
dimCW = width / nxC
dimCH = height / nyC

# Estado de las celdas V = 1, M = 0
gameState = np.zeros((nxC, nyC))

# Automatas de ejemplo

# Palo
# gameState[5, 3] = 1
# gameState[5, 4] = 1
# gameState[5, 5] = 1

# Nave
gameState[10, 3] = 1
gameState[11, 3] = 1
gameState[12, 3] = 1
gameState[12, 2] = 1
gameState[11, 1] = 1

# Control de pausa
pauseExect = True

# Contador de generaciones
num_generation = 0
# Contador de poblacion
num_poblacion = 0

# Loop de ejecucion
while True:
    # Refresco del fondo
    newGameState = np.copy(gameState)
    screen.fill(black)
    time.sleep(0.01)

    # Poblacion
    num_poblacion = np.count_nonzero(newGameState)

    # Registro de eventos de teclado y raton
    if pygame.key.get_focused() and pygame.key.get_pressed()[pygame.K_SPACE]:
        pauseExect = not pauseExect
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    mouseClick = pygame.mouse.get_pressed()
    if sum(mouseClick) > 0:
        posX, posY = pygame.mouse.get_pos()
        celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
        if celX < nxC and celY < nyC:
            newGameState[celX, celY] = not mouseClick[2]
    # Dibujo texto
    font = pygame.font.Font("freesansbold.ttf", 20)
    font_2 = pygame.font.Font("freesansbold.ttf", 10)
    if pauseExect:
        text_pause = font.render("PAUSA", True, white, black)
        screen.blit(text_pause, (height_max - 99, 0))
    else:
        text_pause = font.render("", True, white, black)
        screen.blit(text_pause, (height_max - 99, 0))
    text_gen = font_2.render("GENERACION: " + str(num_generation), True, white, black)
    screen.blit(text_gen, (height_max - 99, 30))
    text_pob = font_2.render("POBLACION: " + str(num_poblacion), True, white, black)
    screen.blit(text_pob, (height_max - 99, 50))
    # Loop por cada celda
    for y in range(0, nxC):
        for x in range(0, nyC):
            if not pauseExect:
                # Calculo de los vecinos
                n_neigh = (
                    gameState[(x - 1) % nxC, (y - 1) % nyC]
                    + gameState[(x) % nxC, (y - 1) % nyC]
                    + gameState[(x + 1) % nxC, (y - 1) % nyC]
                    + gameState[(x - 1) % nxC, (y) % nyC]
                    + gameState[(x + 1) % nxC, (y) % nyC]
                    + gameState[(x - 1) % nxC, (y + 1) % nyC]
                    + gameState[(x) % nxC, (y + 1) % nyC]
                    + gameState[(x + 1) % nxC, (y + 1) % nyC]
                )

                # Regla #1: Una celula muerta con 3 vecinas vivas "revive"
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                # Regla #2: Una celula viva con menos de 2 o mas de 3 vecinas vivas "muere"
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            # Creacion de los poligonos
            poly = [
                ((x) * dimCW, y * dimCH),
                ((x + 1) * dimCW, y * dimCH),
                ((x + 1) * dimCW, (y + 1) * dimCH),
                ((x) * dimCW, (y + 1) * dimCH),
            ]
            # Dibuja los poligonos
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)
    # Actualizacion de generacion
    if not pauseExect:
        num_generation += 1
    # Actualizacion de estado
    gameState = np.copy(newGameState)
    # Actualizacion de ventana
    pygame.display.flip()
