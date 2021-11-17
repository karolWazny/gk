from boilerplate import *
from planets import *

VELOCITY = 400
RADIUS = 80
MASS = 2000000000


class ThreeBodiesRenderer(Renderer):
    def __init__(self):
        redPlanet = Planet(velocity=common.Point(VELOCITY, 0, 0), position=common.Point(0, RADIUS, 0),
                           color=numpy.array([1.0, 0.0, 0.0]), mass=MASS)
        bluePlanet = Planet(velocity=common.Point(-VELOCITY / 2, -VELOCITY / 2 * math.sqrt(3), 0),
                            position=common.Point(RADIUS / 2 * math.sqrt(3), -RADIUS / 2, 0),
                            color=numpy.array([0.0, 0.0, 1.0]), mass=MASS)
        greenPlanet = Planet(velocity=common.Point(-VELOCITY / 2, VELOCITY / 2 * math.sqrt(3), 0),
                             position=common.Point(-RADIUS / 2 * math.sqrt(3), -RADIUS / 2, 0),
                             color=numpy.array([0.0, 1.0, 0.0]), mass=MASS)
        self.system = PlanetSystem(loggingOn=True)
        self.system.planets.append(bluePlanet)
        self.system.planets.append(redPlanet)
        self.system.planets.append(greenPlanet)

    def render(self, time):
        common.axes()
        self.system.updateVelocity()
        self.system.updatePosition()
        self.system.draw()
        # common.spin(0.2)


if __name__ == '__main__':
    main(ThreeBodiesRenderer())
