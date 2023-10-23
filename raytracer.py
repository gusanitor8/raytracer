import pygame
from Obj import *
from pygame.locals import *
from rt import RayTracer
from figures import *
from lights import *
from materials import *

width = 400
height = 400

pygame.init()

screen = pygame.display.set_mode(
    (width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

raytracer = RayTracer(screen)
raytracer.envMap = pygame.image.load("textures/room.jpg")
raytracer.rtClearColor(0.5, 0.5, 0.5)

earthTex = pygame.image.load("textures/earth.jpg")
marbleTex = pygame.image.load("textures/marble.png")

water = Material(diffuse=(0.4, 0.4, 1), spec=256, ks=0.2)
mirror = Material(diffuse=(0.9, 0.9, 0.9), spec=64, ks=0.2, matType=REFLECTIVE)
glossy = Material(diffuse=(0.9, 0.7, 0.9), spec=256, ks=0.2)
glossy2 = Material(diffuse=(0.7, 0.7, 0.9), spec=256, ks=0.2)
earth = Material(texture=earthTex)
marble = Material(diffuse=(0.4, 0.4, 0.4), spec=64, ks=0.2, matType=REFLECTIVE, texture=marbleTex)
glass = Material(diffuse=(0.7, 0.8, 0.9), spec=64, ks=0.2, ior=1.5, matType=TRANSPARENT)

raytracer.scene.append(Plane((0, -10, 0), (0, 1, 0), water))
raytracer.scene.append(Disk((0, -3, -8), (0, 1, 0), 2, mirror))
raytracer.scene.append(AABB((0, 0, -8), (2, 2, 2), glass))
raytracer.scene.append(Sphere((2, 2, -6), 1, earth))
raytracer.scene.append(Triangle(marble, (-3.8, 1.8, -6), (-2, 3, -6), (0, 2, -6)))
raytracer.scene.append(Sphere((2.3, 0, -7), 1, glossy))
raytracer.scene.append(Sphere((-2.3, 0, -7), 1, glossy2))


raytracer.lights.append(AmbientLight(intensity=0.2))
raytracer.lights.append(DirectionalLight(direction=(0, 0, -1), intensity=0.7))
raytracer.lights.append(PointLight(point=(-1, -1, -1), intensity=0.5, color=(1, 0, 1)))


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
            if event.key == pygame.K_s:
                pygame.image.save(screen, "screenshot3.png")

pygame.quit()
