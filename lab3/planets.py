import common
import numpy

TIME_CONSTANT = 0.005
GRAVITY_CONSTANT = 0.00005
NUMBER_OF_LOGS = 1000


class Planet:
    def __init__(self, velocity=common.Point(), mass=100, size=2, position=common.Point(),
                 color=numpy.array([1.0, 1.0, 0.0])):
        self.sphere = common.Sphere(samples=15, scaling=size, mode="lines", translation=position, color=color)
        self.solid = common.Sphere(samples=15, scaling=size, mode="triangles", translation=position,
                                   color=numpy.array([color[0] / 3, color[1] / 3, color[2] / 3]))
        self.mass = mass
        self.velocity = velocity
        self.setPosition(position)
        if color is not None:
            self.sphere.color = color

    def draw(self):
        self.sphere.draw()
        self.solid.draw()

    def updateVelocity(self, otherPlanets=None):
        if otherPlanets is None:
            otherPlanets = []
        deltaV = common.Point()
        for planet in otherPlanets:
            tempVector = planet.getPosition() - self.getPosition()
            partialDeltaV = tempVector.normalized() * planet.mass * (tempVector.length() ** -2)
            deltaV = deltaV + partialDeltaV
        self.velocity = self.velocity + deltaV * GRAVITY_CONSTANT

    def updatePosition(self):
        self.setPosition(self.getPosition() + self.velocity * TIME_CONSTANT)

    def getPosition(self):
        return self.sphere.translation

    def setPosition(self, position):
        self.sphere.translation = position
        self.solid.translation = position

    def logPosition(self):
        pos = self.getPosition()
        return common.Point(x=pos.x, y=pos.y, z=pos.z, r=1.0, g=1.0, b=1.0)


class PlanetSystem:
    def __init__(self, loggingOn=False):
        self.planets = []
        self.loggedPositions = []
        self.loggingOn = loggingOn

    def draw(self):
        for planet in self.planets:
            planet.draw()
        for point in self.loggedPositions:
            point.draw()

    def updateVelocity(self):
        for index in range(0, len(self.planets)):
            planet = self.planets.pop(0)
            planet.updateVelocity(self.planets)
            self.planets.append(planet)

    def updatePosition(self):
        for planet in self.planets:
            planet.updatePosition()
            if self.loggingOn:
                self.loggedPositions.append(planet.logPosition())
        if len(self.loggedPositions) >= NUMBER_OF_LOGS * len(self.planets):
            self.loggedPositions = self.loggedPositions[len(self.planets) * 50:-1]