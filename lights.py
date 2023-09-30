import numpy as np

def reflectVector(direction, normal):
    reflect = 2 * np.dot(direction, normal)
    reflect = np.multiply(reflect, normal)
    reflect = np.subtract(reflect, direction)
    reflect = reflect / np.linalg.norm(reflect)
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
        self.direction = direction / np.linalg.norm(direction)
        super().__init__(intensity, color, "Directional")

    def getDiffuseColor(self, intercept):
        dir = [(i * -1) for i in self.direction]

        intensity = np.dot(intercept.normal, dir) * self.intensity
        intensity = max(0, min(1, intensity))

        diffuseColor = [(i * intensity) for i in self.color]

        return diffuseColor

    def getSpecularColor(self, intercept, viewPos):
        dir = [(i * -1) for i in self.direction]
        reflect = reflectVector(dir, intercept.normal)
        viewDir = np.subtract(viewPos, intercept.point)
        viewDir = viewDir / np.linalg.norm(viewDir)

        specIntensity = max(0, np.dot(viewDir, reflect)) ** intercept.obj.material.spec
        specIntensity *= self.intensity

        specColor = [(i * specIntensity) for i in self.color]
        return specColor
