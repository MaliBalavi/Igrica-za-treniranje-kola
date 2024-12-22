import pygame
import sys
import numpy as np
import random
import math
import pickle 
import pygame.surfarray as surfarray
import copy
from Classes import *

levelnum=2

file_root="levels/"
file_ext = ".pkl"
file_path=file_root+str(levelnum)+file_ext


with open(file_path, 'rb') as f: 
    level = pickle.load(f)
levelcopy=copy.deepcopy(level)
FPS=level.FPS
car=Car(5,40,20,([100,200,255]),1000,10,level.location,3)

pygame.init()
pygame.display.set_caption("Zapis")

screen = pygame.display.set_mode((level.proportions[0],level.proportions[1]))
clock = pygame.time.Clock()

run = True



font = pygame.font.Font(None, 36)


score=0
steps=0
while run:
    level.draw(screen)
    last_screen_array = surfarray.array3d(screen)
    car.show(screen)

    textscore = font.render("Score: "+str(score), True, (255, 255, 255))
    textsteps = font.render("Steps: "+str(steps), True, (255, 255, 255))
    # textstepsapx = font.render("Apx: "+str(round(steps/FPS,2)), True, (255, 255, 255))
    screen.blit(textscore, (50, 50))
    screen.blit(textsteps,(50,100))
    # screen.blit(textstepsapx,(50,200))
    
    car.rfx=0
    car.rfy=0
    car.ni=car.bni



    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run=False               
    

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        car.gas()
    if keys[pygame.K_SPACE]:
        car.brake()
    if keys[pygame.K_a]:
        car.steerleft()
    if keys[pygame.K_d]:
        car.steerright()
    
    car.Ori()
    car.friction(level.g)
    car.ac(level.FPS)
    car.step(level.FPS)
    if car.wallinter(level.walls):
        run=False
    if car.checkinter(level.checkpoints):
        score+=1
    if level.checkall():
        level=copy.deepcopy(levelcopy)
    steps+=1
    pygame.display.flip()
    clock.tick(FPS)

print("Score:"+str(score)+"------------------------------------")
pygame.quit()







