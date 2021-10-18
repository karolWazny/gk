import sys

import numpy as np
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random


class Point:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z


def triangle(vertices=None, color=None):
    if vertices is None:
        vertices = [
            -50, -50, 0,
            50, -50, 0,
            0, 50, 0
        ]
    else:
        vertices = [
            vertices[0].x, vertices[0].y, 0,
            vertices[1].x, vertices[1].y, 0,
            vertices[2].x, vertices[2].y, 0
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
                smallerCoords = Point(coordinates.x + i * smallerDimensions.x, coordinates.y + j * smallerDimensions.y)
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
