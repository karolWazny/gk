import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image

import numpy
import numpy as np

import math

import random

viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

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

showFourthWall = True


class Point:
    def __init__(self, x=0.0, y=0.0, z=0.0, r=1.0, g=1.0, b=1.0):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.g = g
        self.b = b

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z, self.r, self.g, self.b)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z, self.r, self.g, self.b)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other, self.z * other, self.r, self.g, self.b)

    def normalized(self):
        invLength = (self.x ** 2 + self.y ** 2 + self.z ** 2) ** -0.5
        return self * invLength

    def length(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    def draw(self):
        glBegin(GL_POINTS)
        glColor3f(self.r, self.g, self.b)
        glVertex3f(self.x, self.y, self.z)
        glEnd()


class Egg:
    def __init__(self, samples=5, scaling=1, translation=Point(), mode="points", color=None):
        self.showNormals = False
        self.colorWasNone = color is None
        self.translation = translation
        if samples % 2 == 1:
            self.samples = samples
        else:
            self.samples = samples + 1
        self.middleSample = self.samples // 2 + 1

        self.space = np.linspace(0, 1, samples)
        self.scaling = scaling
        self.translation = translation
        rows = []
        normals = []
        uv_points = []
        for u in self.space:
            row, normal_row, uv_row = [], [], []
            for v in self.space:
                point = self.calculate_point(u=u, v=v)
                row.append(point)
                normal_row.append(self.calculate_normal(u, v))
                uv_row.append({"u": u, "v": v})
            rows.append(numpy.array(row))
            normals.append(numpy.array(normal_row))
            uv_points.append(uv_row)
        self.points = numpy.array(rows)
        self.normals = numpy.array(normals)
        self.uv_points = numpy.array(uv_points)

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

    def set_showNormals(self, value):
        self.showNormals = value

    def calculate_normal(self, u, v):
        if u == 0 or u == 1:
            return Point(0, -1, 0)
        if u == 0.5:
            return Point(0, 1, 0)
        u2 = u * u
        u3 = u2 * u
        u4 = u3 * u
        u5 = u4 * u
        pi_v = math.pi * v
        sinpiv = math.sin(pi_v)
        cospiv = math.cos(pi_v)
        x_u = (-450 * u4 + 900 * u3 - 810 * u2 + 360 * u - 45) * cospiv
        x_v = math.pi * (90 * u5 - 225 * u4 + 270 * u3 - 180 * u2 + 45 * u) * sinpiv
        y_u = 640 * u3 - 960 * u2 + 320 * u
        y_v = 0
        z_u = (-450 * u4 + 900 * u3 - 810 * u2 + 360 * u - 45) * sinpiv
        z_v = -math.pi * (90 * u5 - 225 * u4 + 270 * u3 - 180 * u2 + 45 * u) * cospiv

        normal = Point(y_u * z_v - z_u * y_v, z_u * x_v - x_u * z_v, x_u * y_v - y_u * x_v).normalized()

        if u > 0.5:
            normal = normal * -1

        return normal

    def draw(self):
        if self.mode == "lines":
            self.draw_lines()
        elif self.mode == "triangles":
            self.draw_triangles()
        else:
            self.draw_points()
        if self.showNormals:
            self.drawNormals()

    def drawNormals(self):
        glBegin(GL_LINES)
        for row, normRow in zip(self.points, self.normals):
            for vertex, normal in zip(row, normRow):
                vertexToDraw = vertex + self.translation
                normalEnd = vertexToDraw + normal
                glVertex3f(vertexToDraw.x, vertexToDraw.y, vertexToDraw.z)
                glVertex3f(normalEnd.x, normalEnd.y, normalEnd.z)
        glEnd()

    def draw_triangles(self):
        glBegin(GL_TRIANGLES)

        for u in range(0, self.middleSample):

            for v in range(1, self.samples):
                point = self.points[u - 1][v - 1] + self.translation
                pointColor = self.vertexColors[u - 1][v - 1]
                normal = self.normals[u - 1][v - 1]

                secondPoint = self.points[u - 1][v] + self.translation
                secondColor = self.vertexColors[u - 1][v]
                secondNormal = self.normals[u - 1][v]

                belowPoint = self.points[u - 2][v - 1] + self.translation
                belowColor = self.vertexColors[u - 2][v - 1]
                belowNormal = self.normals[u - 2][v - 1]

                abovePoint = self.points[u][v] + self.translation
                aboveColor = self.vertexColors[u][v]
                aboveNormal = self.normals[u][v]

                glColor3f(pointColor[0], pointColor[1], pointColor[2])
                glNormal3f(normal.x, normal.y, normal.z)
                glVertex3f(point.x, point.y, point.z)

                glColor3f(aboveColor[0], aboveColor[1], aboveColor[2])
                glNormal3f(aboveNormal.x, aboveNormal.y, aboveNormal.z)
                glVertex3f(abovePoint.x, abovePoint.y, abovePoint.z)

                glColor3f(secondColor[0], secondColor[1], secondColor[2])
                glNormal3f(secondNormal.x, secondNormal.y, secondNormal.z)
                glVertex3f(secondPoint.x, secondPoint.y, secondPoint.z)

                glColor3f(pointColor[0], pointColor[1], pointColor[2])
                glNormal3f(normal.x, normal.y, normal.z)
                glVertex3f(point.x, point.y, point.z)

                glColor3f(secondColor[0], secondColor[1], secondColor[2])
                glNormal(secondNormal.x, secondNormal.y, secondNormal.z)
                glVertex3f(secondPoint.x, secondPoint.y, secondPoint.z)

                glColor3f(belowColor[0], belowColor[1], belowColor[2])
                glNormal(belowNormal.x, belowNormal.y, belowNormal.z)
                glVertex3f(belowPoint.x, belowPoint.y, belowPoint.z)

        for u in range(self.middleSample, self.samples):

            for v in range(1, self.samples):
                point = self.points[u - 1][v - 1] + self.translation
                pointColor = self.vertexColors[u - 1][v - 1]
                normal = self.normals[u - 1][v - 1]

                secondPoint = self.points[u - 1][v] + self.translation
                secondColor = self.vertexColors[u - 1][v]
                secondNormal = self.normals[u - 1][v]

                belowPoint = self.points[u - 2][v - 1] + self.translation
                belowColor = self.vertexColors[u - 2][v - 1]
                belowNormal = self.normals[u - 2][v - 1]

                abovePoint = self.points[u][v] + self.translation
                aboveColor = self.vertexColors[u][v]
                aboveNormal = self.normals[u][v]

                glColor3f(pointColor[0], pointColor[1], pointColor[2])
                glNormal3f(normal.x, normal.y, normal.z)
                glVertex3f(point.x, point.y, point.z)

                glColor3f(secondColor[0], secondColor[1], secondColor[2])
                glNormal3f(secondNormal.x, secondNormal.y, secondNormal.z)
                glVertex3f(secondPoint.x, secondPoint.y, secondPoint.z)

                glColor3f(aboveColor[0], aboveColor[1], aboveColor[2])
                glNormal3f(aboveNormal.x, aboveNormal.y, aboveNormal.z)
                glVertex3f(abovePoint.x, abovePoint.y, abovePoint.z)

                glColor3f(pointColor[0], pointColor[1], pointColor[2])
                glNormal3f(normal.x, normal.y, normal.z)
                glVertex3f(point.x, point.y, point.z)

                glColor3f(belowColor[0], belowColor[1], belowColor[2])
                glNormal(belowNormal.x, belowNormal.y, belowNormal.z)
                glVertex3f(belowPoint.x, belowPoint.y, belowPoint.z)

                glColor3f(secondColor[0], secondColor[1], secondColor[2])
                glNormal(secondNormal.x, secondNormal.y, secondNormal.z)
                glVertex3f(secondPoint.x, secondPoint.y, secondPoint.z)
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


class TexturedEgg(Egg):
    def draw_triangles(self):
        glBegin(GL_TRIANGLES)

        for u in range(0, self.middleSample):

            for v in range(1, self.samples):
                point = self.points[u - 1][v - 1] + self.translation
                normal = self.normals[u - 1][v - 1]
                uv = self.uv_points[u - 1][v - 1]

                secondPoint = self.points[u - 1][v] + self.translation
                secondNormal = self.normals[u - 1][v]
                second_uv = self.uv_points[u - 1][v]

                belowPoint = self.points[u - 2][v - 1] + self.translation
                belowNormal = self.normals[u - 2][v - 1]
                below_uv = self.uv_points[u - 2][v - 1]

                abovePoint = self.points[u][v] + self.translation
                aboveNormal = self.normals[u][v]
                above_uv = self.uv_points[u][v]

                glNormal3f(normal.x, normal.y, normal.z)
                glTexCoord2f(uv["v"], uv["u"] * 2)
                glVertex3f(point.x, point.y, point.z)

                glNormal3f(aboveNormal.x, aboveNormal.y, aboveNormal.z)
                glTexCoord2f(above_uv["v"], above_uv["u"] * 2)
                glVertex3f(abovePoint.x, abovePoint.y, abovePoint.z)

                glNormal3f(secondNormal.x, secondNormal.y, secondNormal.z)
                glTexCoord2f(second_uv["v"], second_uv["u"] * 2)
                glVertex3f(secondPoint.x, secondPoint.y, secondPoint.z)

                glNormal3f(normal.x, normal.y, normal.z)
                glTexCoord2f(uv["v"], uv["u"] * 2)
                glVertex3f(point.x, point.y, point.z)

                glNormal(secondNormal.x, secondNormal.y, secondNormal.z)
                glTexCoord2f(second_uv["v"], second_uv["u"] * 2)
                glVertex3f(secondPoint.x, secondPoint.y, secondPoint.z)

                glNormal(belowNormal.x, belowNormal.y, belowNormal.z)
                glTexCoord2f(below_uv["v"], below_uv["u"] * 2)
                glVertex3f(belowPoint.x, belowPoint.y, belowPoint.z)

        for u in range(self.middleSample, self.samples):

            for v in range(1, self.samples):
                point = self.points[u - 1][v - 1] + self.translation
                normal = self.normals[u - 1][v - 1]
                uv = self.uv_points[u - 1][v - 1]

                secondPoint = self.points[u - 1][v] + self.translation
                secondNormal = self.normals[u - 1][v]
                second_uv = self.uv_points[u - 1][v]

                belowPoint = self.points[u - 2][v - 1] + self.translation
                belowNormal = self.normals[u - 2][v - 1]
                below_uv = self.uv_points[u - 2][v - 1]

                abovePoint = self.points[u][v] + self.translation
                aboveNormal = self.normals[u][v]
                above_uv = self.uv_points[u][v]

                glNormal3f(normal.x, normal.y, normal.z)
                glTexCoord2f(1 - uv["v"], 1 - uv["u"] * 2)
                glVertex3f(point.x, point.y, point.z)

                glNormal3f(secondNormal.x, secondNormal.y, secondNormal.z)
                glTexCoord2f(1 - second_uv["v"], 1 - 2 * second_uv["u"])
                glVertex3f(secondPoint.x, secondPoint.y, secondPoint.z)

                glNormal3f(aboveNormal.x, aboveNormal.y, aboveNormal.z)
                glTexCoord2f(1 - above_uv["v"], 1 - 2 * above_uv["u"])
                glVertex3f(abovePoint.x, abovePoint.y, abovePoint.z)

                glNormal3f(normal.x, normal.y, normal.z)
                glTexCoord2f(1 - uv["v"], 1 - 2 * uv["u"])
                glVertex3f(point.x, point.y, point.z)

                glNormal(belowNormal.x, belowNormal.y, belowNormal.z)
                glTexCoord2f(1 - below_uv["v"], 1 - 2 * below_uv["u"])
                glVertex3f(belowPoint.x, belowPoint.y, belowPoint.z)

                glNormal(secondNormal.x, secondNormal.y, secondNormal.z)
                glTexCoord2f(1 - second_uv["v"], 1 - 2 * second_uv["u"])
                glVertex3f(secondPoint.x, secondPoint.y, secondPoint.z)
        glEnd()


egg = TexturedEgg(samples=21, mode="triangles", translation=Point(0, -5, 0))


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

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    image = Image.open("piesel_tekstura.tga")

    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, image.size[0], image.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1)
    )


def shutdown():
    pass


def render(time):
    global theta, phi, delta_x, delta_y

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

    egg.draw()

    glFlush()


def update_viewport(window, width, height):
    global pix2angle

    if width == 0:
        width = 1
    if height == 0:
        height = 1
    pix2angle = 360.0 / width

    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, width / height, 0.1, 300.0)
    glViewport(0, 0, width, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global showFourthWall
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if action == GLFW_PRESS and key == GLFW_KEY_1:
        showFourthWall = not showFourthWall


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


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
