class Light(object):
    def __init__(self, intensity=1, color=(1, 1, 1), lightType="None"):
        self.intensity = intensity
        self.color = color
        self.lightType = lightType


class AmbientLight(Light):
    def __init__(self, intensity=0, color=(1, 1, 1)):
        super().__init__(intensity, color, "Ambient")


class DirectionalLight(Light):
    def __init__(self, direction=(0, -1, 0), intensity=1, color=(1, 1, 1)):
        self.direction = direction
        super().__init__(intensity, color, "Directional")
