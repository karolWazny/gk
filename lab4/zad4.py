#!/usr/bin/env python3
import math
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

viewer = [0.0, 0.0, 10.0]

theta = 180.0
phi = 0.0

radius = 10

pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0
delta_y = 0
mouse_y_pos_old = 0

right_mouse_button_pressed = 0
scale = 1.0

modes = {"rotate": 1, "move": 0}
mode = modes["rotate"]


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


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


def example_object():
    glColor3f(1.0, 1.0, 1.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)


def render(time):
    global theta
    global delta_x
    global phi
    global delta_y
    global scale
    global viewer
    global radius

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if mode == modes["rotate"]:
        if left_mouse_button_pressed:
            theta += delta_x * pix2angle
            delta_x = 0

            phi += delta_y * pix2angle
            if phi > 90:
                phi = 90
            elif phi < -90:
                phi = -90

        if right_mouse_button_pressed:
            radius += delta_y / 10
            if radius < 1:
                radius = 1
            elif radius > 50:
                radius = 50

        theta_rad = theta * math.pi / 180
        phi_rad = phi * math.pi / 180

        viewer[0] = radius * math.sin(theta_rad) * math.cos(phi_rad)
        viewer[1] = radius * math.sin(phi_rad)
        viewer[2] = -radius * math.cos(theta_rad) * math.cos(phi_rad)

        gluLookAt(viewer[0], viewer[1], viewer[2],
                  0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    else:
        if left_mouse_button_pressed:
            theta += delta_x * pix2angle
            delta_x = 0

            phi += delta_y * pix2angle
            if phi > 90:
                phi = 90
            elif phi < -90:
                phi = -90

        gluLookAt(viewer[0], viewer[1], viewer[2],
                  0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        if right_mouse_button_pressed:
            scale = scale + delta_y / 100

        glScalef(scale, scale, scale)

        glRotatef(theta, 0.0, 1.0, 0.0)

        matrix = glGetFloat(GL_MODELVIEW_MATRIX)

        glRotatef(phi, matrix[0][0], matrix[1][0], matrix[2][0])

    delta_y = 0

    axes()
    example_object()

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, width / height, 0.1, 300.0)
    glViewport(0, 0, width, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global mode
    global theta
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    elif key == GLFW_KEY_1 and action == GLFW_PRESS:
        print("wciśnięto 1")
        mode = modes["rotate"]
    elif key == GLFW_KEY_2 and action == GLFW_PRESS:
        print("wciśnięto 2")
        mode = modes["move"]


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old
    global delta_y
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed

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