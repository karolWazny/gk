#!/usr/bin/env python3
import math
import sys
import tkinter as tk

import glfw
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

SPEED = 0.7

viewer = [0.0, 0.0, 10.0]
interesting_point = [0.0, 0.0, 0.0]
camera_direction = [0.0, 0.0, 0.0]

theta = 90.0
phi = 0.0

pix2angle = 0.6

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0
delta_y = 0
mouse_y_pos_old = 0

right_mouse_button_pressed = 0
scale = 1.0

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


def render(time, window=None):
    global theta
    global delta_x
    global phi
    global delta_y
    global scale
    global viewer
    global camera_dire
    global move_forward

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    theta -= delta_x * pix2angle
    delta_x = 0

    phi -= delta_y * pix2angle
    if phi > 90:
        phi = 90
    elif phi < -90:
        phi = -90

    theta_rad = theta * math.pi / 180
    phi_rad = phi * math.pi / 180

    move_forward = 0
    move_right = 0
    move_up = 0

    if glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS:
        move_forward = 1
    elif glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS:
        move_forward = -1

    if glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS:
        move_right = 1
    elif glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS:
        move_right = -1

    if glfwGetKey(window, GLFW_KEY_SPACE) == GLFW_PRESS:
        move_up = 1
    elif glfwGetKey(window, GLFW_KEY_LEFT_CONTROL) == GLFW_PRESS:
        move_up = -1

    camera_direction[0] = math.sin(theta_rad) * math.cos(phi_rad)
    camera_direction[1] = math.sin(phi_rad)
    camera_direction[2] = math.cos(theta_rad) * math.cos(phi_rad)

    viewer[0] += (camera_direction[0] * move_forward - camera_direction[2] * move_right) * SPEED
    viewer[1] += (camera_direction[1] * move_forward + move_up) * SPEED
    viewer[2] += (camera_direction[2] * move_forward + camera_direction[0] * move_right) * SPEED

    interesting_point[0] = viewer[0] + camera_direction[0]
    interesting_point[1] = viewer[1] + camera_direction[1]
    interesting_point[2] = viewer[2] + camera_direction[2]

    gluLookAt(viewer[0], viewer[1], viewer[2],
              interesting_point[0], interesting_point[1], interesting_point[2], 0.0, 1.0, 0.0)

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
    global theta
    global move_forward
    global move_right
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)



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
    root = tk.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(screen_width, screen_height, __file__, glfw.get_primary_monitor(), None)
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
    update_viewport(window, screen_width, screen_height)
    glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)
    glfwSetInputMode(window, GLFW_STICKY_KEYS, GLFW_TRUE)
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), window)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()

if __name__ == '__main__':
    main()
