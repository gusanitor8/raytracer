import numpy as np
from math import acos, asin

def reflectVector(direction, normal):
    reflect = 2 * np.dot(direction, normal)
    reflect = np.multiply(reflect, normal)
    reflect = np.subtract(reflect, direction)
    reflect = reflect / np.linalg.norm(reflect)
    return reflect

def totalInternalReflection(incident, normal, n1, n2):
    if n1 < n2:
        n1, n2 = n2, n1

    ai = acos(np.dot(incident, normal))
    ac = asin(n2/n1)

    return ai >= ac

def refractVector(incident, normal, n1, n2):
    # Snells law
    refract = np.multiply(np.dot(incident, normal), normal)
    refract = np.subtract(incident, refract)
    refract = n1 * refract
    refract = refract / n2

    refract = refract/np.linalg.norm(refract)
    return refract

def fresnel(n1,n2):
    kr = ((n1**0.5 - n2**0.5)**2)/((n1**0.5 + n2**0.5)**2)
    kt = 1 - kr

    return kr, kt

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
        self.direction = direction / np.linalg.norm(direction)
        super().__init__(intensity, color, "Directional")

    def getDiffuseColor(self, intercept):
        dir = [(i * -1) for i in self.direction]

        intensity = np.dot(intercept.normal, dir) * self.intensity
        intensity = max(0, min(1, intensity))
        intensity *= 1 - intercept.obj.material.ks
        diffuseColor = [(i * intensity) for i in self.color]

        return diffuseColor

    def getSpecularColor(self, intercept, viewPos):
        dir = [(i * -1) for i in self.direction]
        reflect = reflectVector(dir, intercept.normal)
        viewDir = np.subtract(viewPos, intercept.point)
        viewDir = viewDir / np.linalg.norm(viewDir)

        specIntensity = max(0, np.dot(viewDir, reflect)) ** intercept.obj.material.spec
        specIntensity *= intercept.obj.material.ks
        specIntensity *= self.intensity

        specColor = [(i * specIntensity) for i in self.color]
        return specColor


class PointLight(Light):
    def __init__(self, point=(0, 0, 0), intensity=1, color=(1, 1, 1)):
        self.point = point
        super().__init__(intensity, color, "Point")

    def getDiffuseColor(self, intercept):
        dir = np.subtract(self.point, intercept.point)
        R = np.linalg.norm(dir)
        dir = dir / R

        intensity = np.dot(intercept.normal, dir) * self.intensity
        intensity *= 1 - intercept.obj.material.ks

        # ley de cuadrados inversos
        # If = intensity/R^2
        # R es la distancia entre el punto intercepto a la luz de punto

        if R != 0:
            intensity /= R**2
        intensity = max(0, min(1, intensity))

        return [(i * intensity) for i in self.color]

    def getSpecularColor(self, intercept, viewPos):
        dir = np.subtract(self.point, intercept.point)
        R = np.linalg.norm(dir)
        dir = dir / R

        reflect = reflectVector(dir, intercept.normal)

        viewDir = np.subtract(viewPos, intercept.point)
        viewDir = viewDir / np.linalg.norm(viewDir)

        specIntensity = max(0, np.dot(viewDir, reflect)) ** intercept.obj.material.spec
        specIntensity *= intercept.obj.material.ks
        specIntensity *= self.intensity

        if R != 0:
            specIntensity /= R**2
        specIntensity = max(0, min(1, specIntensity))

        specColor = [(i * specIntensity) for i in self.color]
        return specColor
