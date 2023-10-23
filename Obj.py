import numpy as np

class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()

        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        for line in self.lines:
            try:
                prefix, value = line.split(" ", 1)
                value = value.strip()
            except:
                continue

            if prefix == "v":  # vertices
                self.vertices.append(list(map(float, value.split(" "))))
            elif prefix == "vn":  # normals
                self.normals.append(list(map(float, value.split(" "))))
            elif prefix == "vt":
                self.texcoords.append(list(map(float, value.split(" "))))
            elif prefix == "f":
                self.faces.append([list(map(int, vert.split("/"))) for vert in value.split(" ")])


    def transform_vertices(self, translate=(0,0,0), rotate=(0,0,0), scale=(1,1,1)):
        pass