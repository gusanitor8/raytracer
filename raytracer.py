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
marbleTex = pygame.image.load("textures/marble.png")

brick = Material(diffuse=(1, 0.4, 0.4), spec=8, ks=0.01)
grass = Material(diffuse=(0.4, 0.6, 0.4), spec=32, ks=0.1)
color = Material(diffuse=(0.7, 0.6, 0.4), spec=32, ks=0.1)
color2 = Material(diffuse=(0.4, 0.6, 0.7), spec=32, ks=0.1)
color3 = Material(diffuse=(0.7, 0.4, 0.6), spec=32, ks=0.1)
color4 = Material(diffuse=(0.4, 0.7, 0.6), spec=32, ks=0.1)
color5 = Material(diffuse=(0.6, 0.4, 0.7), spec=32, ks=0.1)

water = Material(diffuse=(0.4, 0.4, 1), spec=256, ks=0.2)
mirror = Material(diffuse=(0.9, 0.9, 0.9), spec=64, ks=0.2, matType=REFLECTIVE)
earth = Material(texture=earthTex)
marble = Material(diffuse=(0.4, 0.4, 0.4), spec=64, ks=0.2, matType=REFLECTIVE, texture=marbleTex)
glass = Material(diffuse=(0.7, 0.8, 0.9), spec=64, ks=0.2, ior=1.5, matType=TRANSPARENT)

raytracer.scene.append(Triangle(v0=(2, -1, -10), v1=(0, 2, -10), v2=(-2, -1, -10), material=brick))


raytracer.lights.append(AmbientLight(intensity=0.4))
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
                pygame.image.save(screen, "screenshot1.bmp")

pygame.quit()
