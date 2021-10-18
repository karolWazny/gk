import sys

import numpy as np
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


def triangle():
    # Triangle
    x1, x2, x3 = 30, 70, 50
    y1, y2, y3 = 20, 50, 70

    vertices = [
        -50, -50, 0,
        50, -50, 0,
        0, 50, 0
    ]

    v = np.array(vertices, dtype=np.float32)
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, v)

    glDrawArrays(GL_TRIANGLES, 0, 3)

    # glColor3f(0.5, 0.5, 0.0)
    # glPointSize(3.0)
    # glBegin(GL_LINES)
    #
    # glVertex2f(x1, y1)
    # glVertex2f(x2, y2)
    #
    # glVertex2f(x2, y2)
    # glVertex2f(x3, y3)
    #
    # glVertex2f(x3, y3)
    # glVertex2f(x1, y1)
    #
    # glEnd()
    # glFlush()
