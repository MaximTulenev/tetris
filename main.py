import pygame, random, sys, time
from pygame.locals import *

# окно

window_W = 600
window_H = 500
cup_W = 10
cup_H = 20
block = 20
window_full = pygame.display.set_mode((window_W, window_H))

side_margin = int((window_W - cup_W * block) / 2)
top_margin = int((window_H - cup_H * block))
WHITE = (255, 255, 255)
window_cup = pygame.draw.polygon(window_full, WHITE, ((side_margin, window_H), (side_margin, top_margin - window_H), (side_margin + cup_W * block, window_H - top_margin), (side_margin + cup_W * block, window_H)))

while True:
    pygame.display.update()