from math import tan, pi
import mathlib as ml
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
        y = self.width - y

        if (0 <= x < self.width and 0 <= y < self.height):
            if color != None:
                color = (color[0]*255,
                         color[1]*255,
                         color[2]*255)

                self.screen.set_at((x, y), color)

            else:
                self.screen.set_at((x, y), self.currColor)

    def rtCastRay(self, orig, dir, sceneObj=None):
        depth = float('inf')
        intercept = None
        hit = None

        for obj in self.scene:
            if sceneObj != obj:
                intercept = obj.ray_intersect(orig, dir)
                if intercept != None:
                    if intercept.distance < depth:
                        hit = intercept
                        depth = intercept.distance

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
                    direction = [i / ml.norm(direction) for i in direction]

                    intercept = self.rtCastRay(self.camPosirion, direction)

                    if intercept != None:
                        # phong reflection model
                        # Light Color = Ambient + Diffuse + LightColor
                        # FinalColor = SurfaceColor  * LightColor

                        surfaceColor = intercept.obj.material.diffuse
                        ambientLightColor = [0,0,0]
                        diffuseLightColor = [0,0,0]
                        specularLightColor = [0,0,0]

                        for light in self.lights:
                            if light.lightType == "Ambient":
                                ambientLightColor = [ambientLightColor[i] + light.getLightColor()[i] for i in range(3)]

                            else:
                                shadowIntersect = None
                                lightDir = None
                                if light.lightType == "Directional":
                                    lightDir = [(i * -1) for i in light.direction]
                                elif light.lightType == "Point":
                                    lightDir = ml.subtract(light.point, intercept.point)
                                    # lightDir = lightDir/ np.linalg.norm(lightDir)
                                    lightDir = [i / ml.norm(lightDir) for i in lightDir]

                                shadowIntersect = self.rtCastRay(intercept.point, lightDir, intercept.obj)

                                if shadowIntersect == None:
                                    diffuseLightColor = [diffuseLightColor[i] + light.getDiffuseColor(intercept)[i] for i in range(3)]
                                    specularLightColor = [(specularLightColor[i] + light.getSpecularColor(intercept, self.camPosirion)[i]) for i in range(3)]


                        lightColor = [ambientLightColor[i] + diffuseLightColor[i] + specularLightColor[i] for i in range(3)]
                        finalColor = [min(1, surfaceColor[i] * lightColor[i]) for i in range(3)]

                        self.rtPoint(x, y, finalColor)