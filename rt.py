from math import tan, pi
import numpy as np


class RayTracer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.scene = []
        self.camPosirion = [0, 0, 0]
        self.rtViewPort(0, 0, self.width, self.height)  # check on me
        self.rtProjection()

        self.rtColor(1, 1, 1)
        self.rtClearColor(0, 0, 0)
        self.rtClear()

        self.lights = []

    def rtViewPort(self, posX, posY, width, height):
        self.vpX = posX
        self.vpY = posY
        self.vpWidth = width
        self.vpHeight = height

    def rtProjection(self, fov=60, n=0.1):
        aspectRatio = self.vpWidth / self.vpHeight
        self.nearPlane = n
        self.topEdge = tan((fov * pi / 180)/2) * self.nearPlane
        self.rightEdge = self.topEdge * aspectRatio

    # color de fondo

    def rtClearColor(self, r, g, b):
        self.clearColor = (r*255, g*255, b*255)

    def rtClear(self):
        self.screen.fill(self.clearColor)

    # color de los objetos
    def rtColor(self, r, g, b):
        self.currColor = (r*255, g*255, b*255)

    def rtPoint(self, x, y, color=None):
        if (0 <= x < self.width and 0 <= y < self.height):
            if color != None:
                color = (color[0]*255,
                         color[1]*255,
                         color[2]*255)

                self.screen.set_at((x, y), color)

            else:
                self.screen.set_at((x, y), self.currColor)

    def rtCastRay(self, orig, dir):
        intercept = None
        hit = None

        for obj in self.scene:
            intercept = obj.ray_intersect(orig, dir)
            if intercept != None:
                hit = intercept

        return hit

    def rtRender(self):
        for x in range(self.vpX, self.vpX + self.vpWidth + 1):
            for y in range(self.vpY, self.vpY + self.vpHeight + 1):
                if 0 <= x < self.width and 0 <= y < self.height:
                    # pasar de coordenadas de ventana
                    # a coordenadas NDC (-1 a 1)
                    pX = ((x + 0.5 - self.vpX) / self.vpWidth) * 2 - 1
                    pY = ((y + 0.5 - self.vpY) / self.vpHeight) * 2 - 1

                    pX *= self.rightEdge
                    pY *= self.topEdge

                    # crear un rayo
                    direction = (pX, pY, -self.nearPlane)
                    direction = direction / np.linalg.norm(direction)

                    intercept = self.rtCastRay(self.camPosirion, direction)

                    if intercept != None:
                        material = intercept.obj.material
                        colorP = material.diffuse

                        for light in self.lights:
                            if light.lightType == "Ambient":
                                colorP[0] *= light.intensity * light.color[0]
                                colorP[1] *= light.intensity * light.color[1]
                                colorP[2] *= light.intensity * light.color[2]

                            elif light.lightType == "Directional":
                                lightDir = np.array(light.direction) * -1
                                lightDir = lightDir / np.linalg.norm(lightDir)
                                intensity = np.dot(lightDir, intercept.normal)
                                intensity = max(0, min(1, intensity))

                                colorP[0] *= intensity
                                colorP[1] *= intensity
                                colorP[2] *= intensity

                        self.rtPoint(x, y, colorP)
