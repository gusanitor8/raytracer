import numpy as np
import mathlib as ml
from math import atan2, acos, pi


class Intercept(object):
    def __init__(self, distance, point, normal, texcoords, obj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texcoords = texcoords
        self.obj = obj


class Shape(object):
    def __init__(self, position, material):
        self.material = material
        self.position = position

    def ray_intersect(self, orig, dir):
        return None


class Sphere(Shape):
    def __init__(self, position, radius, material):
        self.radius = radius
        super().__init__(position, material)

    def ray_intersect(self, orig, dir):
        L = ml.subtract(self.position, orig)
        lengthL = ml.norm(L)
        tca = ml.dot(L, dir)
        d = (lengthL ** 2 - tca ** 2) ** 0.5

        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d ** 2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None

        P = ml.add(orig, t0 * ml.array(dir))
        normal = ml.subtract(P, self.position)  # why?
        normal = normal / ml.norm(normal)

        u = (atan2(normal[2], normal[0]) / (2 * pi)) + 0.5
        v = acos(normal[1]) / pi

        return Intercept(distance=t0, point=P, normal=normal, texcoords=(u, v), obj=self)


class Plane(Shape):
    def __init__(self, position, normal, material):
        self.normal = normal
        super().__init__(position, material)

    def ray_intersect(self, orig, dir):
        # distancia = ((planePos - origRay) o normal) / (dirRay o normal)
        denom = ml.dot(dir, self.normal)

        if abs(denom) <= 0.0001:
            return None

        num = ml.dot(ml.subtract(self.position, orig), self.normal)
        t = num / denom

        if t < 0:
            return None

        P = ml.add(orig, t * ml.array(dir))

        return Intercept(distance=t,
                         point=P,
                         normal=self.normal,
                         texcoords=None,
                         obj=self)


class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        self.radius = radius
        super().__init__(position, normal, material)

    def ray_intersect(self, orig, dir):
        planeIntersect = super().ray_intersect(orig, dir)

        if planeIntersect is None:
            return None

        contactDistance = ml.subtract(planeIntersect.point, self.position)
        contactDistance = ml.norm(contactDistance)

        if contactDistance > self.radius:
            return None

        return Intercept(distance=planeIntersect.distance,
                         point=planeIntersect.point,
                         normal=self.normal,
                         texcoords=None,
                         obj=self)


class AABB(Shape):
    def __init__(self, position, size, material):
        super().__init__(position, material)

        self.planes = []
        self.size = size
        self.lengthX = size[0]
        self.lengthY = size[1]
        self.lengthZ = size[2]

        leftPlane = Plane(ml.add(self.position, (-self.lengthX / 2, 0, 0)), (-1, 0, 0), material)
        rightPlane = Plane(ml.add(self.position, (self.lengthX / 2, 0, 0)), (1, 0, 0), material)

        bottomPlane = Plane(ml.add(self.position, (0, -self.lengthY / 2, 0)), (0, -1, 0), material)
        topPlane = Plane(ml.add(self.position, (0, self.lengthY / 2, 0)), (0, 1, 0), material)

        backPlane = Plane(ml.add(self.position, (0, 0, -self.lengthZ / 2)), (0, 0, -1), material)
        frontPlane = Plane(ml.add(self.position, (0, 0, self.lengthZ / 2)), (0, 0, 1), material)

        self.planes.append(leftPlane)
        self.planes.append(rightPlane)
        self.planes.append(bottomPlane)
        self.planes.append(topPlane)
        self.planes.append(backPlane)
        self.planes.append(frontPlane)

        # bound
        self.boundsMin = [0, 0, 0]
        self.boundsMax = [0, 0, 0]

        bias = 0.0001

        for i in range(3):
            self.boundsMin[i] = self.position[i] - (size[i] / 2 + bias)
            self.boundsMax[i] = self.position[i] + (size[i] / 2 + bias)

    def ray_intersect(self, orig, dir):
        t = float('inf')
        intersect = None
        bias = 0.001

        u = 0
        v = 0

        for plane in self.planes:
            planeIntersect = plane.ray_intersect(orig, dir)

            if planeIntersect is not None:
                planePoint = planeIntersect.point

                if self.boundsMin[0] < planePoint[0] < self.boundsMax[0]:
                    if self.boundsMin[1] < planePoint[1] < self.boundsMax[1]:
                        if self.boundsMin[2] < planePoint[2] < self.boundsMax[2]:
                            if planeIntersect.distance < t:
                                t = planeIntersect.distance
                                intersect = planeIntersect

                                # generar las uvs
                                if abs(plane.normal[0]) > 0:
                                    # estoy en X, usamos Y y Z para generar las uvs
                                    u = (planePoint[1] - self.boundsMin[1]) / (self.size[1] + bias * 2)
                                    v = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + bias * 2)

                                elif abs(plane.normal[1]) > 0:
                                    # esyoy en Y, usamos X y Z para generar las uvs
                                    u = (planePoint[0] - self.boundsMin[0]) / (self.size[0]+ bias * 2)
                                    v = (planePoint[2] - self.boundsMin[2]) / (self.size[2]+ bias * 2)

                                elif abs(plane.normal[2]) > 0:
                                    # estoy en Z, usamos X y Y para generar las uvs
                                    u = (planePoint[0] - self.boundsMin[0]) / (self.size[0]+ bias * 2)
                                    v = (planePoint[1] - self.boundsMin[1]) / (self.size[1]+ bias * 2)

        if intersect is None:
            return None

        return Intercept(distance=t,
                         point=intersect.point,
                         normal=ml.array(intersect.normal),
                         texcoords=(u, v),
                         obj=self)
