import numpy as np
import mathlib as ml


def reflectVector(direction, normal):
    reflect = 2 * ml.dot(direction, normal)
    reflect = ml.multiply(reflect, normal)
    reflect = ml.subtract(reflect, direction)
    reflect = reflect / ml.norm(reflect)
    return reflect


class Light(object):
    def __init__(self, intensity=1, color=(1, 1, 1), lightType="None"):
        self.intensity = intensity
        self.color = color
        self.lightType = lightType

    def getLightColor(self):
        return [self.color[0] * self.intensity,
                self.color[1] * self.intensity,
                self.color[2] * self.intensity]

    def getDiffuseColor(self, intercept):
        return None

    def getSpecularColor(self, intercept, viewPos):
        return None


class AmbientLight(Light):
    def __init__(self, intensity=0, color=(1, 1, 1)):
        super().__init__(intensity, color, "Ambient")


class DirectionalLight(Light):
    def __init__(self, direction=(0, -1, 0), intensity=1, color=(1, 1, 1)):
        self.direction = [i / ml.norm(direction) for i in direction]
        super().__init__(intensity, color, "Directional")

    def getDiffuseColor(self, intercept):
        dir = [(i * -1) for i in self.direction]

        intensity = ml.dot(intercept.normal, dir) * self.intensity
        intensity = max(0, min(1, intensity))
        intensity *= 1 - intercept.obj.material.ks
        diffuseColor = [(i * intensity) for i in self.color]

        return diffuseColor

    def getSpecularColor(self, intercept, viewPos):
        dir = [(i * -1) for i in self.direction]
        reflect = reflectVector(dir, intercept.normal)
        viewDir = ml.subtract(viewPos, intercept.point)
        viewDir = viewDir / ml.norm(viewDir)

        specIntensity = max(0, ml.dot(viewDir, reflect)) ** intercept.obj.material.spec
        specIntensity *= intercept.obj.material.ks
        specIntensity *= self.intensity

        specColor = [(i * specIntensity) for i in self.color]
        return specColor


class PointLight(Light):
    def __init__(self, point=(0, 0, 0), intensity=1, color=(1, 1, 1)):
        self.point = point
        super().__init__(intensity, color, "Point")

    def getDiffuseColor(self, intercept):
        dir = ml.subtract(self.point, intercept.point)
        R = ml.norm(dir)
        dir = dir / R

        intensity = ml.dot(intercept.normal, dir) * self.intensity
        intensity *= 1 - intercept.obj.material.ks

        # ley de cuadrados inversos
        # If = intensity/R^2
        # R es la distancia entre el punto intercepto a la luz de punto

        if R != 0:
            intensity /= R**2
        intensity = max(0, min(1, intensity))

        return [(i * intensity) for i in self.color]

    def getSpecularColor(self, intercept, viewPos):
        dir = ml.subtract(self.point, intercept.point)
        R = ml.linalg.norm(dir)
        dir = dir / R

        reflect = reflectVector(dir, intercept.normal)

        viewDir = ml.subtract(viewPos, intercept.point)
        viewDir = viewDir / ml.linalg.norm(viewDir)

        specIntensity = max(0, ml.dot(viewDir, reflect)) ** intercept.obj.material.spec
        specIntensity *= intercept.obj.material.ks
        specIntensity *= self.intensity

        if R != 0:
            specIntensity /= R**2
        specIntensity = max(0, min(1, specIntensity))

        specColor = [(i * specIntensity) for i in self.color]
        return specColor
