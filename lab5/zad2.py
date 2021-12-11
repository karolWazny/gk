#!/usr/bin/env python3
import sys

import glfw
import numpy
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


first_component_index = 0
second_component_index = 0


stuff_changed = False
cursor_changed = False


light_components = numpy.array([light_ambient, light_diffuse, light_specular])
component_names = ['ambient', 'diffuse', 'specular']


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)


def shutdown():
    pass


def render(time):
    global theta, stuff_changed, delta_x, cursor_changed

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        delta_x = 0

    if stuff_changed:
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_components[0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_components[1])
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_components[2])

        print(light_components)
        print('Choice:', component_names[first_component_index], second_component_index)
        stuff_changed = False

    if cursor_changed:
        print('Choice:', component_names[first_component_index], second_component_index)
        cursor_changed = False

    glRotatef(theta, 0.0, 1.0, 0.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global first_component_index, second_component_index, stuff_changed, cursor_changed
    if action == GLFW_PRESS:
        if key == GLFW_KEY_ESCAPE:
            glfwSetWindowShouldClose(window, GLFW_TRUE)
        elif key == GLFW_KEY_1:
            first_component_index = 0
            cursor_changed = True
        elif key == GLFW_KEY_2:
            first_component_index = 1
            cursor_changed = True
        elif key == GLFW_KEY_3:
            first_component_index = 2
            cursor_changed = True
        elif key == GLFW_KEY_4:
            first_component_index = 3
            cursor_changed = True
        elif key == glfw.KEY_RIGHT:
            second_component_index = (second_component_index + 1) % 4
            cursor_changed = True
        elif key == glfw.KEY_LEFT:
            second_component_index = (second_component_index - 1) % 4
            cursor_changed = True
        elif key == glfw.KEY_UP:
            light_components[first_component_index][second_component_index] += 0.1
            if light_components[first_component_index][second_component_index] > 1.0:
                light_components[first_component_index][second_component_index] = 1.0
            stuff_changed = True
        elif key == glfw.KEY_DOWN:
            light_components[first_component_index][second_component_index] -= 0.1
            if light_components[first_component_index][second_component_index] < 0.0:
                light_components[first_component_index][second_component_index] = 0.0
            stuff_changed = True

def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
