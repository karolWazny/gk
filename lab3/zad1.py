import numpy

from boilerplate import *
import common


class FirstRenderer(Renderer):
    def __init__(self):
        self.egg = common.Egg(samples=50, scaling=16, translation=common.Point(0, -70, 0))

    def render(self, time):
        common.axes()
        self.egg.draw()
        common.spin(0.1)

if __name__ == '__main__':
    main(FirstRenderer())
