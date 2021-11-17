import numpy
import numpy as np
from OpenGL.GL import *
import random

from OpenGL.raw.GLUT import glutSwapBuffers


class Point:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other, self.z * other)

    def normalized(self):
        invLength = (self.x ** 2 + self.y ** 2 + self.z ** 2) ** -0.5
        return self * invLength

    def length(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    def draw(self):
        glBegin(GL_POINTS)
        glColor3f(1.0, 1.0, 1.0)
        glVertex3f(self.x, self.y, self.z)
        glEnd()


def triangle(vertices=None, color=None):
    if vertices is None:
        vertices = [
            -50, -50, 0,
            50, -50, 0,
            0, 50, 0
        ]
    else:
        vertices = [
            vertices[0].x, vertices[0].y, vertices[0].z,
            vertices[1].x, vertices[1].y, vertices[1].z,
            vertices[2].x, vertices[2].y, vertices[2].z
        ]
    if color is None:
        glColor3f(0.9, 0.9, 0.9)
    else:
        glColor3f(color[0], color[1], color[2])

    v = np.array(vertices, dtype=np.float32)
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, v)

    glDrawArrays(GL_TRIANGLES, 0, 3)


def colorTriangle(verticesList=None, colorArray=None):
    if verticesList is None:
        vertices = [
            -50, -50, 0,
            50, -50, 0,
            0, 50, 0
        ]
    else:
        vertices = verticesList

    if colorArray is None:
        colors = [
            0, 1, 0,
            1, 0, 0,
            0, 0, 1.0
        ]
    else:
        colors = colorArray

    v = np.array(vertices, dtype=np.float32)
    c = np.array(colors, dtype=np.float32)

    glEnableClientState(GL_COLOR_ARRAY)
    glColorPointer(3, GL_FLOAT, 0, c)

    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, v)

    glDrawArrays(GL_TRIANGLES, 0, 3)


def rectangle(x=0, y=0, a=1, b=1, d=0.0, color=None):
    halfB = b / 2
    halfA = a / 2
    deltaX = d * halfA
    firstTriangle = [
        Point(x + halfA + deltaX, y + halfB, 0),
        Point(x + halfA - deltaX, y - halfB, 0),
        Point(x - halfA - deltaX, y - halfB, 0)
    ]

    secondTriangle = [
        Point(x - halfA - deltaX, y - halfB, 0),
        Point(x - halfA + deltaX, y + halfB, 0),
        Point(x + halfA + deltaX, y + halfB, 0)
    ]

    triangle(firstTriangle, color)
    triangle(secondTriangle, color)


class ColoredRectangle:
    def __init__(self, coordinates=None, dimensions=None, distortion=0.0):
        if dimensions is None:
            self.dimensions = Point(1, 1)
        else:
            self.dimensions = dimensions
        if coordinates is None:
            self.coordinates = Point(0, 0)
        else:
            self.coordinates = coordinates

        self.colors = []
        for i in range(0, 4):
            for j in range(0, 3):
                self.colors.append(random.random())
        self.distortion = distortion

    def draw(self):
        x = self.coordinates.x
        y = self.coordinates.y
        halfB = self.dimensions.x / 2
        halfA = self.dimensions.y / 2
        deltaX = self.distortion * halfA
        colors = []
        for index in range(0, 9):
            colors.append(self.colors[index])
        vertices = [
            x + halfA + deltaX, y + halfB, 0,
            x + halfA - deltaX, y - halfB, 0,
            x - halfA - deltaX, y - halfB, 0
        ]
        colorTriangle(vertices, colors)
        colors = []
        for index in range(6, 12):
            colors.append(self.colors[index])
        for index in range(0, 3):
            colors.append(self.colors[index])
        vertices = [
            x - halfA - deltaX, y - halfB, 0,
            x - halfA + deltaX, y + halfB, 0,
            x + halfA + deltaX, y + halfB, 0
        ]
        colorTriangle(vertices, colors)


class Sierpinski:
    def __init__(self, coordinates=None, dimensions=None, depth=1, color1=None, color2=None):
        if dimensions is None:
            self.dimensions = Point(1, 1)
        else:
            self.dimensions = dimensions
        if coordinates is None:
            self.coordinates = Point(0, 0)
        else:
            self.coordinates = coordinates
        self.depth = depth
        if color1 is None:
            self.color1 = [1.0, 1.0, 1.0]
        else:
            self.color1 = color1
        if color2 is None:
            self.color2 = [0.0, 0.0, 0.0]
        else:
            self.color2 = color2

    def draw(self):
        rectangle(self.coordinates.x, self.coordinates.y, self.dimensions.x, self.dimensions.y, color=self.color1)
        self.holesRecursively(self.dimensions, self.coordinates, self.depth)

    def holesRecursively(self, dimensions, coordinates, depth):
        if depth == 0:
            return
        smallerDimensions = Point(dimensions.x / 3, dimensions.y / 3)
        rectangle(x=coordinates.x, y=coordinates.y, a=dimensions.x / 3, b=dimensions.y / 3, color=self.color2)
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not not (i or j):
                    smallerCoords = Point(coordinates.x + i * smallerDimensions.x,
                                          coordinates.y + j * smallerDimensions.y)
                    self.holesRecursively(smallerDimensions, smallerCoords, depth - 1)


class IteratedFunction:
    functions = [
        {'a': -0.67, 'b': -0.02, 'c': 0.00, 'd': -0.18, 'e': 0.81, 'f': 10.0},
        {'a': 0.40, 'b': 0.40, 'c': 0.00, 'd': -0.10, 'e': 0.40, 'f': 0.0},
        {'a': -0.40, 'b': -0.40, 'c': 0.00, 'd': -0.10, 'e': 0.40, 'f': 0.0},
        {'a': -0.10, 'b': 0.0, 'c': 0.00, 'd': 0.44, 'e': 0.44, 'f': -2.0}
    ]

    def __init__(self, startingPoint=None, steps=10):
        if startingPoint is None:
            self.point = Point()
        else:
            self.point = startingPoint
        self.steps = steps
        self.randomState = random.getstate()

    def drawPoint(self):
        glColor3f(0.9, 0.9, 0.9)
        glPointSize(1.0)
        glBegin(GL_POINTS)
        glVertex2f(self.point.x, self.point.y)
        glEnd()

    def transformPoint(self):
        i = random.randrange(0, 4)
        fi = self.functions[i]
        x = self.point.x
        y = self.point.y
        self.point.x = fi['a'] * x + fi['b'] * y + fi['c']
        self.point.y = fi['d'] * x + fi['e'] * y + fi['f']

    def draw(self):
        random.setstate(self.randomState)
        for index in range(0, self.steps):
            self.drawPoint()
            self.transformPoint()


def axes():
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)
    glEnd()


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


class Egg:
    def __init__(self, samples=5, scaling=1, translation=Point(), mode="points", color=None):
        self.colorWasNone = color is None
        self.translation = translation
        self.samples = samples
        self.space = np.linspace(0, 1, samples)
        self.scaling = scaling
        self.translation = translation
        rows = []
        for u in self.space:
            row = []
            for v in self.space:
                point = self.calculate_point(u=u, v=v)
                row.append(point)
            rows.append(numpy.array(row))
        self.points = numpy.array(rows)

        self.vertexColors = None
        if mode == "triangles" and color is None:
            rows = []
            for u in range(0, samples):
                row = []
                for v in range(0, samples):
                    vertexColor = numpy.array([random.random(), random.random(), random.random()])
                    row.append(vertexColor)
                rows.append(numpy.array(row))
            self.vertexColors = numpy.array(rows)

            for u in range(0, samples):
                self.vertexColors[u][0] = self.vertexColors[samples - u - 1][-1]
        self.mode = mode

        if color is not None:
            self.color = color
        else:
            self.color = numpy.array([1.0, 1.0, 0.0])

    def draw(self):
        if self.mode == "lines":
            self.draw_lines()
        elif self.mode == "triangles":
            self.draw_triangles()
        else:
            self.draw_points()

    def draw_triangles(self):
        glBegin(GL_TRIANGLES)

        if self.colorWasNone:
            for u in range(0, self.samples):

                for v in range(1, self.samples):
                    point = self.points[u - 1][v - 1] + self.translation
                    pointColor = self.vertexColors[u - 1][v - 1]

                    secondPoint = self.points[u - 1][v] + self.translation
                    secondColor = self.vertexColors[u - 1][v]

                    belowPoint = self.points[u - 2][v - 1] + self.translation
                    belowColor = self.vertexColors[u - 2][v - 1]

                    abovePoint = self.points[u][v] + self.translation
                    aboveColor = self.vertexColors[u][v]

                    glColor3f(pointColor[0], pointColor[1], pointColor[2])
                    glVertex3f(point.x, point.y, point.z)

                    glColor3f(secondColor[0], secondColor[1], secondColor[2])
                    glVertex3f(secondPoint.x, secondPoint.y, secondPoint.z)

                    glColor3f(aboveColor[0], aboveColor[1], aboveColor[2])
                    glVertex3f(abovePoint.x, abovePoint.y, abovePoint.z)

                    glColor3f(pointColor[0], pointColor[1], pointColor[2])
                    glVertex3f(point.x, point.y, point.z)

                    glColor3f(secondColor[0], secondColor[1], secondColor[2])
                    glVertex3f(secondPoint.x, secondPoint.y, secondPoint.z)

                    glColor3f(belowColor[0], belowColor[1], belowColor[2])
                    glVertex3f(belowPoint.x, belowPoint.y, belowPoint.z)
        else:
            glColor3f(self.color[0], self.color[1], self.color[2])
            for u in range(0, self.samples):

                for v in range(1, self.samples):
                    point = self.points[u - 1][v - 1] + self.translation

                    secondPoint = self.points[u - 1][v] + self.translation

                    belowPoint = self.points[u - 2][v - 1] + self.translation

                    abovePoint = self.points[u][v] + self.translation

                    glVertex3f(point.x, point.y, point.z)
                    glVertex3f(secondPoint.x, secondPoint.y, secondPoint.z)
                    glVertex3f(abovePoint.x, abovePoint.y, abovePoint.z)

                    glVertex3f(point.x, point.y, point.z)
                    glVertex3f(secondPoint.x, secondPoint.y, secondPoint.z)
                    glVertex3f(belowPoint.x, belowPoint.y, belowPoint.z)
        glEnd()

    def draw_lines(self):
        glBegin(GL_LINES)
        glColor3f(self.color[0], self.color[1], self.color[2])
        for u in range(0, self.samples):
            for v in range(1, self.samples):
                point = self.points[u - 1][v - 1] + self.translation

                nextPoint = self.points[u - 1][v] + self.translation
                glVertex3f(point.x, point.y, point.z)
                glVertex3f(nextPoint.x, nextPoint.y, nextPoint.z)

                nextPoint = self.points[u][v - 1] + self.translation
                glVertex3f(point.x, point.y, point.z)
                glVertex3f(nextPoint.x, nextPoint.y, nextPoint.z)
        glEnd()

    def draw_points(self):
        glBegin(GL_POINTS)
        glColor3f(self.color[0], self.color[1], self.color[2])
        for row in self.points:
            for point in row:
                drawnPoint = point + self.translation
                glVertex3f(drawnPoint.x, drawnPoint.y, drawnPoint.z)
        glEnd()

    def calculate_point(self, u, v):
        return Point(self.x_from(u, v), self.y_from(u, v), self.z_from(u, v))

    def x_from(self, u, v):
        u2 = u * u
        u3 = u2 * u
        u4 = u3 * u
        u5 = u4 * u
        return (-90 * u5 + 225 * u4 - 270 * u3 + 180 * u2 - 45 * u) * numpy.cos(numpy.pi * v) * self.scaling

    def y_from(self, u, v):
        u2 = u * u
        u3 = u2 * u
        u4 = u3 * u
        return (160 * u4 - 320 * u3 + 160 * u2) * self.scaling

    def z_from(self, u, v):
        u2 = u * u
        u3 = u2 * u
        u4 = u3 * u
        u5 = u4 * u
        return (-90 * u5 + 225 * u4 - 270 * u3 + 180 * u2 - 45 * u) * numpy.sin(numpy.pi * v) * self.scaling


class Sphere(Egg):
    def x_from(self, u, v):
        return numpy.sin(numpy.pi * v) * numpy.sin(2 * numpy.pi * u) * self.scaling

    def y_from(self, u, v):
        return -numpy.cos(2 * numpy.pi * u) * self.scaling

    def z_from(self, u, v):
        return numpy.sin(2 * numpy.pi * u) * numpy.cos(numpy.pi * v) * self.scaling
