import math
import sys

import numpy as np
from OpenGL.raw.GLUT import GLUT_DEPTH, glutInitDisplayMode
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

import common

theta = 0.0
phi = 0.0

delta_x = 0
delta_y = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
left_mouse_button_pressed = 0
PIXEL_TO_ANGLE_COEFF = 300
PIXEL_TO_ANGLE = 0
points_scrolled = 0


def update_viewport(window, width, height):
    global PIXEL_TO_ANGLE
    if height == 0:
        height = 1
    if width == 0:
        width = 1
    aspectRatio = width / height
    PIXEL_TO_ANGLE = PIXEL_TO_ANGLE_COEFF / width
    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()
    gluPerspective(60, aspectRatio, 1.0, 1000000.0)
    glTranslatef(0.0, 0.0, -200.0)
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
        global delta_x
        global delta_y
        global points_scrolled

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # W tym przykładzie jest to wyczyszczenie ramki w pamięci –glClear()
        self.render(time)
        # Następnie zawartość pamięci jest przesyłana do wyświetlenia –glFlush()

        if left_mouse_button_pressed:
            modelViewMatrix = glGetFloat(GL_MODELVIEW_MATRIX)
            angle_x = delta_x * PIXEL_TO_ANGLE
            glRotatef(angle_x, modelViewMatrix[0][1], modelViewMatrix[1][1], modelViewMatrix[2][1])
            delta_x = 0

            angle_y = delta_y * PIXEL_TO_ANGLE
            glRotatef(angle_y, modelViewMatrix[0][0], modelViewMatrix[1][0], modelViewMatrix[2][0])
            delta_y = 0
        else:
            common.spin(0.15)

        if points_scrolled != 0:
            glMatrixMode(GL_PROJECTION)
            glTranslatef(0.0, 0.0, 10 * points_scrolled)
            glMatrixMode(GL_MODELVIEW)
            points_scrolled = 0

        glFlush()
        # Najistotniejsza funkcja programu

    def render(self, time):
        pass


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global delta_y
    global mouse_x_pos_old
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_scroll_callback(window, x_offset, y_offset):
    global points_scrolled
    points_scrolled += y_offset

def pre_run():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetScrollCallback(window, mouse_scroll_callback)
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
