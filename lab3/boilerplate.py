import sys

import numpy as np
from OpenGL.raw.GLUT import GLUT_DEPTH, glutInitDisplayMode
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random


def update_viewport(window, width, height):
    if height == 0:
        height = 1
    if width == 0:
        width = 1
    aspectRatio = width / height
    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()
    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspectRatio, 100.0 / aspectRatio, 1000.0, -1000.0)
    else:
        glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0, 1000.0, -1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def startup():
    # Ustawiamy wartość koloru, do jakiego będzie czyszczony bufor.
    glClearColor(0, 0, 0.1, 0.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glClearDepth(1.0)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    update_viewport(None, 400, 400)


def shutdown():
    # zawiera instrukcję, która nic nie robi –tak zwany placeholder
    pass


class Renderer:
    def render_and_display(self, time):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # W tym przykładzie jest to wyczyszczenie ramki w pamięci –glClear()
        self.render(time)
        # Następnie zawartość pamięci jest przesyłana do wyświetlenia –glFlush()
        glFlush()
        # Najistotniejsza funkcja programu

    def render(self, time):
        pass


def pre_run():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)

    glfwSwapInterval(1)
    startup()
    return window


def run(window, renderer=None):
    if renderer is None:
        renderer = Renderer()
    while not glfwWindowShouldClose(window):
        renderer.render_and_display(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()


def post_run():
    shutdown()
    glfwTerminate()


def main(renderer=None):
    window = pre_run()

    run(window, renderer)

    post_run()
