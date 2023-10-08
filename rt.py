import random
from math import tan, atan2, acos, pi
import mathlib as ml
from materials import *
from lights import *
import random
import pygame

MAX_RECURSION_DEPTH = 3

class RayTracer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.scene = []
        self.lights = []

        self.camPosirion = [0, 0, 0]
        self.rtViewPort(0, 0, self.width, self.height)  # check on me
        self.rtProjection()

        self.rtColor(1, 1, 1)
        self.rtClearColor(0, 0, 0)
        self.rtClear()

        self.envMap = None



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

    def rtCastRay(self, orig, dir, sceneObj=None, recursion = 0):

        if recursion >= MAX_RECURSION_DEPTH:
            return None

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

    def rtRayColor(self, intercept, rayDirection, recursion = 0):
        if intercept == None:
            if self.envMap:
                x = (atan2(rayDirection[2], rayDirection[0])/ (2 * pi) + 0.5) * self.envMap.get_width()
                y = acos(rayDirection[1]) / pi * self.envMap.get_height()
                envColor = self.envMap.get_at((int(x), int(y)))

                return [envColor[i]/255 for i in range(3)]
            else:
                return None

        # phong reflection model
        # Light Color = Ambient + Diffuse + LightColor
        # FinalColor = SurfaceColor  * LightColor

        material = intercept.obj.material

        surfaceColor = material.diffuse
        if material.texture and intercept.texcoords:
            tX = intercept.texcoords[0] *  material.texture.get_width()
            tY = intercept.texcoords[1] * material.texture.get_height()

            texColor = material.texture.get_at((int(tX), int(tY)))
            texColor = [i/ 255 for i in texColor]
            surfaceColor = [surfaceColor[i] * texColor[i] for i in range(3)]




        reflectColor = [0,0,0]
        refractColor = [0,0,0]
        ambientLightColor = [0, 0, 0]
        diffuseLightColor = [0, 0, 0]
        specularLightColor = [0, 0, 0]
        finalColor = [0,0,0]

        if material.matType == OPAQUE:

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
                        lightDir = lightDir / ml.norm(lightDir)

                    shadowIntersect = self.rtCastRay(intercept.point, lightDir, intercept.obj)

                    if shadowIntersect == None:
                        diffuseLightColor = [diffuseLightColor[i] + light.getDiffuseColor(intercept)[i] for i in range(3)]
                        specularLightColor = [
                            (specularLightColor[i] + light.getSpecularColor(intercept, self.camPosirion)[i]) for i in
                            range(3)]



        elif material.matType == REFLECTIVE:
            reflect = reflectVector(ml.array(rayDirection) * -1, intercept.normal)
            reflectIntercept = self.rtCastRay(intercept.point, reflect, intercept.obj, recursion + 1)
            reflectColor = self.rtRayColor(reflectIntercept, reflect, recursion + 1)

            for light in self.lights:
                if light.lightType != "Ambient":
                    lightDir = None
                    if light.lightType == "Directional":
                        lightDir = [(i * -1) for i in light.direction]
                    elif light.lightType == "Point":
                        lightDir = ml.subtract(light.point, intercept.point)
                        lightDir = lightDir / ml.norm(lightDir)

                    shadowIntersect = self.rtCastRay(intercept.point, lightDir, intercept.obj)

                    if shadowIntersect == None:
                        specularLightColor = [
                            (specularLightColor[i] + light.getSpecularColor(intercept, self.camPosirion)[i]) for i in
                            range(3)]

        elif material.matType == TRANSPARENT:
            outside = ml.dot(rayDirection, intercept.normal) < 0
            bias = intercept.normal * 0.001

            # reflection
            reflect = reflectVector(rayDirection, ml.array(intercept.normal) * -1)
            reflectOrig = ml.add(intercept.point, bias) if outside else ml.subtract(intercept.point, bias)
            reflectIntercept = self.rtCastRay(reflectOrig, reflect, None, recursion + 1)
            reflectColor = self.rtRayColor(reflectIntercept, reflect, recursion + 1)

            for light in self.lights:
                if light.lightType != "Ambient":
                    lightDir = None
                    if light.lightType == "Directional":
                        lightDir = [(i * -1) for i in light.direction]
                    elif light.lightType == "Point":
                        lightDir = ml.subtract(light.point, intercept.point)
                        lightDir = lightDir / ml.norm(lightDir)

                    shadowIntersect = self.rtCastRay(intercept.point, lightDir, intercept.obj)

                    if shadowIntersect == None:
                        specularLightColor = [
                            (specularLightColor[i] + light.getSpecularColor(intercept, self.camPosirion)[i]) for i in
                            range(3)]

            if not totalInternalReflection(intercept.normal, rayDirection, 1.0, material.ior):
                refract = refractVector(intercept.normal, rayDirection, 1.0, material.ior)
                refractOrig = ml.subtract(intercept.point, bias) if outside else ml.add(intercept.point, bias)
                refractIntercept = self.rtCastRay(refractOrig, refract, None, recursion + 1)
                refractColor = self.rtRayColor(refractIntercept, refract, recursion + 1)

                kr, kt = fresnel(intercept.normal, rayDirection, 1.0, material.ior)
                reflectColor = ml.multiply(reflectColor, kr)
                refractColor = ml.multiply(refractColor, kt)

            pass

        lightColor = [
            ambientLightColor[i] + diffuseLightColor[i] + specularLightColor[i] + reflectColor[i] + refractColor[i] for
            i in range(3)]
        finalColor = [min(1, (surfaceColor[i] * lightColor[i])) for i in range(3)]

        return finalColor

    def rtRender(self):
        indices =  [(i, j) for i in range(self.vpWidth) for j in range(self.vpHeight)]
        random.shuffle(indices)

        for i, j in indices:
            x = i + self.vpX
            y = j + self.vpY

            if 0 <= x < self.width and 0 <= y < self.height:
                # pasar de coordenadas de ventana
                # a coordenadas NDC (-1 a 1)
                pX = ((x + 0.5 - self.vpX) / self.vpWidth) * 2 - 1
                pY = ((y + 0.5 - self.vpY) / self.vpHeight) * 2 - 1

                pX *= self.rightEdge
                pY *= self.topEdge

                # crear un rayo
                direction = (pX, pY, -self.nearPlane)
                dir_magnitude = ml.norm(direction)
                direction = [direction[i]/dir_magnitude for i in range(3)]

                intercept = self.rtCastRay(self.camPosirion, direction)
                rayColor = self.rtRayColor(intercept, direction)

                if rayColor != None:
                    self.rtPoint(x, y, rayColor)
                    pygame.display.flip()