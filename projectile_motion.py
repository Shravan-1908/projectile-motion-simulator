from enum import Enum
import math
import numpy as np


class Constant(Enum):
    g = 9.8  # m/s^2
    RE = 6.37e6  # radius of earth in meters


class GroundToGround:
    def __init__(
        self,
        initial_velocity: float,
        angle_of_projection: float,
        horizontal_acceleration: float,
        vertical_acceleration: float = -Constant.g.value,
        planet_radius: float = Constant.RE
    ) -> None:
        """
        Angle of projection must be in degrees.
        The other two parameters are in m/s and m/s^2 resp.
        """
        # convert angle into radians
        self.angle = angle_of_projection * math.pi / 180

        self.ux = initial_velocity * math.cos(self.angle)
        self.uy = initial_velocity * math.sin(self.angle)

        # acceleration due to gravity
        self.ay = -abs(vertical_acceleration)
        self.ax = horizontal_acceleration

    @property
    def time_of_flight(self):
        return (2 * self.uy) / abs(self.ay)

    @property
    def range(self) -> float:
        return (self.ux * self.time_of_flight) + (
            0.5 * self.ax * (self.time_of_flight**2)
        )

    @property
    def hmax(self) -> float:
        return (self.uy**2) / (2 * abs(self.ay))

    def coordinates(self, t: float):
        x = (self.ux * t) + (0.5 * self.ax * (t**2))
        y = (self.uy * t) + (0.5 * self.ay * (t**2))
        return x, y

    def velocity(self, coordinate: tuple[int, int]):
        """
        Returns the velocity of the object at the given coordinate.
        """
        x, y = coordinate
        vx_squared = (self.ux**2) + (2 * self.ax * x)
        vy_squared = (self.uy**2) + (2 * self.ay * y)

        return math.sqrt(vx_squared + vy_squared)

    def trajectory(self, timestep: float) -> list[tuple[int, int]]:
        """
        Timestep should be in seconds, it represents 1/framerate.
        """
        coordinates_list = []
        for t in np.arange(0.0, self.time_of_flight, timestep):
            c = self.coordinates(t)
            if c[0] < 0 or c[1] < 0:
                break
            coordinates_list.append(c)

        return coordinates_list


if __name__ == "__main__":
    g2g = GroundToGround(40, 3, 0)
    print(g2g.angle)
    print(g2g.range)
    print(g2g.hmax)
    print(g2g.time_of_flight)
