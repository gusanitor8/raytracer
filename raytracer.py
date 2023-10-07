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
raytracer.envMap = pygame.image.load("textures/room.jpg")
raytracer.rtClearColor(0.5, 0.5, 0.5)

earthTex = pygame.image.load("textures/earth.jpg")

brick = Material(diffuse=(1, 0.4, 0.4), spec=8, ks=0.01)
grass = Material(diffuse=(0.4, 1, 0.4), spec=32, ks=0.1)
water = Material(diffuse=(0.4, 0.4, 1), spec=256, ks=0.2)
mirror = Material(diffuse=(0.9, 0.9, 0.9), spec=64, ks=0.2, matType=REFLECTIVE)
earth = Material(texture=earthTex)
glass = Material(diffuse=(0.9, 0.9, 0.9), spec=64, ks=0.2, ior=1.5, matType=TRANSPARENT)

# raytracer.scene.append(Sphere(position=(-2, 0, -5), radius=1, material=brick))
# raytracer.scene.append(Sphere(position=(2, 2, -5), radius=0.5, material=grass))
# raytracer.scene.append(Sphere(position=(0, 0, -7), radius=2, material=earth))
raytracer.scene.append(Sphere(position=(-2, 0, -7), radius=2, material=glass))
raytracer.scene.append(Sphere(position=(2, 0, -7), radius=2, material=mirror))

raytracer.lights.append(AmbientLight(intensity=0.1))
raytracer.lights.append(DirectionalLight(direction=(-1, -1, -1), intensity=0.7))
raytracer.lights.append(PointLight(point=(5, 0, -5), intensity=0.5, color=(1, 0, 1)))

raytracer.rtClear()
raytracer.rtRender()

print("\n Render Time: ", pygame.time.get_ticks() / 1000, "secs")

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

pygame.quit()
