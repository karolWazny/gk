import numpy

from boilerplate import *
import common


class SecondRenderer(Renderer):
    def __init__(self):
        self.egg = common.Egg(samples=30, scaling=8, translation=common.Point(0, -35, 0), mode="lines")

    def render(self, time):
        common.axes()
        self.egg.draw()
        common.spin(numpy.sqrt(time) * 0.05)

if __name__ == '__main__':
    main(SecondRenderer())
