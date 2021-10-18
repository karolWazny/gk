import sys
from glfw.GLFW import *
from OpenGL.GL import *

from lab2.shapes import IteratedFunction

x, y = 0, 0
steps = 10_000

system = IteratedFunction(steps=steps)

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
        glOrtho(-100.0, 100.0, -100.0 / aspectRatio, 100.0 / aspectRatio, 1.0, -1.0)
    else:
        glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0, 1.0, -1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def startup():
    # Ustawiamy wartość koloru, do jakiego będzie czyszczony bufor.
    glClearColor(0, 0, 0, 1.0)
    update_viewport(None, 400, 400)


def shutdown():
    # zawiera instrukcję, która nic nie robi –tak zwany placeholder
    pass


def render(time):
    # W tym przykładzie jest to wyczyszczenie ramki w pamięci –glClear()
    glClear(GL_COLOR_BUFFER_BIT)
    # Następnie zawartość pamięci jest przesyłana do wyświetlenia –glFlush()
    system.draw()
    glFlush()
    # Najistotniejsza funkcja programu


def main():
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
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
