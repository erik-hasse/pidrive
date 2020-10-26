from abc import ABC


class Car(ABC):
    def __init__(self, drive_motors, turning_motors, **sensors):
        self._drive_motors = drive_motors
        self._turning_motors = turning_motors
        for k, v in sensors.items():
            setattr(self, k, v)

        self.velocity = 0
        self.angle = 0

    def stop(self):
        self.speed = 0

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, new):
        for m in self._turning_motors:
            m.angle = new
        self._angle = new

    @property
    def speed(self):
        return self._drive_motors[0].speed

    @speed.setter
    def speed(self, new):
        for m in self._drive_motors:
            m.speed = new

    @property
    def velocity(self):
        return self._drive_motors[0].velocity

    @velocity.setter
    def velocity(self, new):
        for m in self._drive_motors:
            m.velocity = new

    @property
    def direction(self):
        return self._drive_motors[0].direction

    @direction.setter
    def direction(self, new):
        for m in self._drive_motors:
            m.direction = new
