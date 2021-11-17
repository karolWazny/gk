import numpy

from boilerplate import *
import common
from planets import *


class FourthRenderer(Renderer):
    def __init__(self):
        sun = Planet(mass=100_000_000, size=8, color=numpy.array([1.0, 1.0, 0.0]))
        redPlanet = Planet(velocity=common.Point(0, 0, 70), position=common.Point(180, 20, 0),
                           color=numpy.array([1.0, 0.0, 0.0]), mass=40000)
        bluePlanet = Planet(velocity=common.Point(0, 0, 130), position=common.Point(50, 0, 0),
                            color=numpy.array([0.0, 0.0, 1.0]))
        greenPlanet = Planet(velocity=common.Point(0, 0, 100), position=common.Point(90, -10, 0),
                             color=numpy.array([0.0, 1.0, 0.0]), mass=50)
        purpleComet = Planet(velocity=common.Point(0, 0, 300), position=common.Point(15, -15, 0),
                             color=numpy.array([1.0, 0.0, 1.0]), mass=10, size=0.3)
        self.system = PlanetSystem(loggingOn=True)
        self.system.planets.append(sun)
        self.system.planets.append(bluePlanet)
        self.system.planets.append(redPlanet)
        self.system.planets.append(greenPlanet)
        self.system.planets.append(purpleComet)

    def render(self, time):
        common.axes()
        self.system.updateVelocity()
        self.system.updatePosition()
        self.system.draw()


if __name__ == '__main__':
    main(FourthRenderer())
