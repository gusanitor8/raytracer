import pygame
from pygame.locals import *
from rt import RayTracer
from figures import *
from lights import *
from materials import *

width = 256
height = 256

pygame.init()

screen = pygame.display.set_mode(
    (width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

raytracer = RayTracer(screen)
raytracer.rtClearColor(0.5, 0.5, 0.5)

carrot = Material(diffuse=(1, 0.4, 0.4), spec=8, ks=0.01)
snow = Material(diffuse=(1, 1, 1), spec=32, ks=0.1)
charcoal = Material(diffuse=(0.2, 0.2, 0.2), spec=256, ks=0.2)

# shapes
# body
raytracer.scene.append(Sphere(position=(0, 1.5, -5), radius=0.7, material=snow))
raytracer.scene.append(Sphere(position=(0, 0, -5), radius=1, material=snow))
raytracer.scene.append(Sphere(position=(0, -2, -5), radius=1.5, material=snow))

#buttons
raytracer.scene.append(Sphere(position=(0, 0, -3), radius=0.15, material=charcoal))
raytracer.scene.append(Sphere(position=(0, -1, -3), radius=0.15, material=charcoal))
raytracer.scene.append(Sphere(position=(0, -0.5, -3), radius=0.15, material=charcoal))

# face
# nose
raytracer.scene.append(Sphere(position=(0, 1.27, -4), radius=0.13, material=carrot))

# eyes
raytracer.scene.append(Sphere(position=(-0.25, 1.4, -4), radius=0.13, material=snow))
raytracer.scene.append(Sphere(position=(-0.25, 1.4, -3.9), radius=0.07, material=charcoal))

raytracer.scene.append(Sphere(position=(0.25, 1.4, -4), radius=0.13, material=snow))
raytracer.scene.append(Sphere(position=(0.25, 1.4, -3.9), radius=0.07, material=charcoal))

#smile
raytracer.scene.append(Sphere(position=(-0.25, 1.1, -3.9), radius=0.05, material=charcoal))
raytracer.scene.append(Sphere(position=(0.25, 1.1, -3.9), radius=0.05, material=charcoal))

raytracer.scene.append(Sphere(position=(0.1, 1, -3.9), radius=0.05, material=charcoal))
raytracer.scene.append(Sphere(position=(-0.1, 1, -3.9), radius=0.05, material=charcoal))

#lights
raytracer.lights.append(AmbientLight(intensity=0.7))
raytracer.lights.append(DirectionalLight(direction=(-1, -1, -1), intensity=0.7))


isRunning = True

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False


        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_s:
                pygame.image.save(screen, "imagen.bmp")

    raytracer.rtClear()
    raytracer.rtRender()
    pygame.display.flip()


pygame.quit()
