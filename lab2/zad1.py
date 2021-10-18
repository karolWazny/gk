import sys
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy
from shapes import colorTriangle


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
    glClearColor(0, 0, 0.1, 1.0)
    update_viewport(None, 400, 400)


def shutdown():
    # zawiera instrukcję, która nic nie robi –tak zwany placeholder
    pass


def render(time):
    # W tym przykładzie jest to wyczyszczenie ramki w pamięci –glClear()
    glClear(GL_COLOR_BUFFER_BIT)
    # Następnie zawartość pamięci jest przesyłana do wyświetlenia –glFlush()
    colorTriangle()
    glFlush()
    # Najistotniejsza funkcja programu


def main():
    """
    Najpierw następuje przygotowanie biblioteki GLFW –glfwInit().
    - Jeśli to z jakiegoś powodu się nie powiedzie, kończymy program
    """
    if not glfwInit():
        sys.exit(-1)
    """
    Następnie utworzone zostaje okno, w którym wyświetlany będzie obraz.
    - Pierwsze dwa argumenty to początkowy rozmiar okna,
    - trzeci argument to tytuł okna –tutaj będzie to nazwa naszego pliku,
    - dwa ostatnie argumenty nie są dla nas interesujące na etapie zajęć.
    - W przypadku niepowodzenia, tu również kończymy program.
    """
    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)
    """
    Kolejne wywołanie określa miejsce aktywnego obecnie kontekstu OpenGL,
    - czyli w którym miejscu generowany będzie przez nas obraz,
    - biblioteka GLFW pozwala stworzyć kilka okien na raz i je przełączać
    """
    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)

    """
    glfwSwapInterval() włącza tak zwaną synchronizację pionową.
    - Wpływa na funkcję glfwSwapBuffers(), ogranicza szybkość
    """
    glfwSwapInterval(1)
    startup()
    """
    Dalej następuje główna część programu, powtarzana do zamknięcia okna.
    - W pętli wykonujemy funkcję render() i podmieniamy ramki obrazu.
    - Dodatkowo przetworzone zostaną zaistniałe zdarzenia okien i wejść.
    """
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()
    """
    odpowiada za uruchomienie głównej funkcji
    –Wywołanie to następuję tylko przy bezpośrednim odpaleniu skryptu.
    - Przydatne jest to na wyższym etapie wtajemniczenia w mowie węży :-)
    """


if __name__ == '__main__':
    main()

    """
    •  Domyślna przestrzeń rysowania w OpenGL obejmuje zakres [-1.0; 1.0] 
    każdej osi.
    •  Poniższy kod przekształca ten przedział do [-100.0; 100.0] dla osi X i Y
    """