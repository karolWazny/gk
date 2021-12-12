#!/usr/bin/env python3
import math
import sys

import numpy
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from lab5 import common

viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0
pix2angle = 1.0

radius = 10

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light0_ambient = [0.1, 0.1, 0.0, 1.0]
light0_diffuse = [0.8, 0.8, 0.0, 1.0]
light0_specular = [1.0, 1.0, 1.0, 1.0]
light0_position = [0.0, 0.0, 10.0, 1]

att0_constant = 1.0
att0_linear = 0.05
att0_quadratic = 0.001

light1_ambient = [0.0, 0.1, 0.1, 1.0]
light1_diffuse = [0.0, 0.0, 0.8, 1.0]
light1_specular = [1.0, 1.0, 1.0, 1.0]
light1_position = [10.0, 0.0, -10.0, 1]

att1_constant = 1.0
att1_linear = 0.05
att1_quadratic = 0.001

light_positions = numpy.array([{'phi': 40.0, 'theta': 0.0, 'xyz': light0_position, 'id': GL_LIGHT0},
                               {'phi': 0.0, 'theta': 40.0, 'xyz': light1_position, 'id': GL_LIGHT1}])

chosen_light = 0
chosen_light_changed = False


egg = common.Egg(scaling=0.5, mode="triangles", samples=21, translation=common.Point(0, -2.2, 0))
egg.set_showNormals(True)

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    for index in range(0, 2):
        xyz_pos = light_positions[index]['xyz']

        theta_rad = light_positions[index]['theta'] * math.pi / 180
        phi_rad = light_positions[index]['phi'] * math.pi / 180

        xyz_pos[0] = radius * math.sin(theta_rad) * math.cos(phi_rad)
        xyz_pos[1] = radius * math.sin(phi_rad)
        xyz_pos[2] = -radius * math.cos(theta_rad) * math.cos(phi_rad)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light0_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light0_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light0_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light0_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att0_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att0_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att0_quadratic)

    glLightfv(GL_LIGHT1, GL_AMBIENT, light1_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light1_diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light1_specular)
    glLightfv(GL_LIGHT1, GL_POSITION, light1_position)

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att1_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att1_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att1_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)


def shutdown():
    pass


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


def render(time):
    global theta, phi, delta_x, delta_y, chosen_light_changed

    if chosen_light_changed:
        print("Chosen light:", chosen_light + 1)
        chosen_light_changed = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        delta_x = 0
        phi += delta_y * pix2angle
        if phi > 90:
            phi = 90
        if phi < -90:
            phi = -90
        delta_y = 0

    glRotatef(theta, 0.0, 1.0, 0.0)

    matrix = glGetFloat(GL_MODELVIEW_MATRIX)
    glRotatef(phi, matrix[0][0], matrix[1][0], matrix[2][0])

    glLightfv(light_positions[0]['id'], GL_POSITION, light_positions[0]['xyz'])
    glLightfv(light_positions[1]['id'], GL_POSITION, light_positions[1]['xyz'])

    if right_mouse_button_pressed:
        light_positions[chosen_light]['theta'] -= delta_x * pix2angle
        delta_x = 0
        light_positions[chosen_light]['phi'] -= delta_y * pix2angle
        if light_positions[chosen_light]['phi'] > 90:
            light_positions[chosen_light]['phi'] = 90
        if light_positions[chosen_light]['phi'] < -90:
            light_positions[chosen_light]['phi'] = -90
        delta_y = 0

        xyz_pos = light_positions[chosen_light]['xyz']

        theta_rad = light_positions[chosen_light]['theta'] * math.pi / 180
        phi_rad = light_positions[chosen_light]['phi'] * math.pi / 180

        xyz_pos[0] = radius * math.sin(theta_rad) * math.cos(phi_rad)
        xyz_pos[1] = radius * math.sin(phi_rad)
        xyz_pos[2] = -radius * math.cos(theta_rad) * math.cos(phi_rad)

        glLightfv(light_positions[chosen_light]['id'], GL_POSITION, xyz_pos)


    # quadric = gluNewQuadric()
    # gluQuadricDrawStyle(quadric, GLU_FILL)
    # gluSphere(quadric, 3.0, 10, 10)
    # gluDeleteQuadric(quadric)

    egg.draw()

    glTranslatef(light0_position[0], light0_position[1], light0_position[2])
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.6, 10, 10)
    gluDeleteQuadric(quadric)
    glTranslatef(-light0_position[0], -light0_position[1], -light0_position[2])


    glTranslatef(light1_position[0], light1_position[1], light1_position[2])
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.6, 10, 10)
    gluDeleteQuadric(quadric)
    glTranslatef(-light1_position[0], -light1_position[1], -light1_position[2])

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, width / height, 0.1, 300.0)
    glViewport(0, 0, width, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global chosen_light, chosen_light_changed
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if action == GLFW_PRESS:
        if key == GLFW_KEY_1:
            chosen_light = 0
            chosen_light_changed = True
        elif key == GLFW_KEY_2:
            chosen_light = 1
            chosen_light_changed = True
        elif key == GLFW_KEY_Q:
            egg.set_showNormals(True)
        elif key == GLFW_KEY_W:
            egg.set_showNormals(False)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed, right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT:
        if action == GLFW_PRESS:
            left_mouse_button_pressed = 1
        else:
            left_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT:
        if action == GLFW_PRESS:
            right_mouse_button_pressed = 1
        else:
            right_mouse_button_pressed = 0


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
