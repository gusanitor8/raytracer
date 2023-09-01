import pygame
from pygame.locals import *
from rt import RayTracer
from figures import *

width = 256
height = 256

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

raytracer = RayTracer(screen)
raytracer.rtClearColor(0.5, 0.5, 0.5)

raytracer.scene.append(Sphere( position = (0,0,-5), radius = 1 ))


isRunning = True

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
    

    raytracer.rtClear()    
    raytracer.rtRender()
    pygame.display.flip()


pygame.quit()