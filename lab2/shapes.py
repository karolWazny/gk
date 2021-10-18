import sys

import numpy as np
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


class Point:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z


def triangle(vertices=None):
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

    v = np.array(vertices, dtype=np.float32)
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, v)

    glDrawArrays(GL_TRIANGLES, 0, 3)


def colorTriangle():
    vertices = [
        -50, -50, 0,
        50, -50, 0,
        0, 50, 0
    ]

    colors = [
        0, 1, 0,
        1, 0, 0,
        0, 0, 1.0
    ]

    v = np.array(vertices, dtype=np.float32)
    c = np.array(colors, dtype=np.float32)

    glEnableClientState(GL_COLOR_ARRAY)
    glColorPointer(3, GL_FLOAT, 0, c)

    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, v)

    glDrawArrays(GL_TRIANGLES, 0, 3)


def rectangle(x=0, y=0, a=1, b=1, d=0.0):
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

    triangle(firstTriangle)
    triangle(secondTriangle)
