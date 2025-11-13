import sys
import pygame
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Fight Club Tic-Tac-Toe")

WINDOW_size = (400, 400)

screen = pygame.display.set_mode(WINDOW_size, 0, 32)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.update()