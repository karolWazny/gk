import numpy

from boilerplate import *
import common


class SecondRenderer(Renderer):
    def __init__(self):
        self.egg = common.Egg(samples=30, scaling=16, translation=common.Point(0, -70, 0), mode="lines")

    def render(self, time):
        common.axes()
        self.egg.draw()

if __name__ == '__main__':
    main(SecondRenderer())
