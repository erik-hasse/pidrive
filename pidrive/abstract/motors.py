from abc import ABC, abstractmethod

from pidrive.types import Direction


class DriveMotor(ABC):
    """An abstract class for a drive motor.

    Two methods must by implemented: _set_speed and _set_direction:

        * _set_speed is called when speed is set. A value between 0 and
            max_speed (inclusive is passed). The implementation should
            interact with the hardware to set the speed of the motor.
        * _set_direction is called when direction is set. Either
            Direction.Forward or Direction.Backward is passed. The
            implementation should interact with the hardware to set the
            direction of the motor.

    Args:
        max_speed (int): The value which will correspond with the maximum
            speed of the motor. This does not inherently limit the speed,
            although an implementation may use it that way.

    """

    def __init__(self, max_speed):
        self._max_speed = max_speed
        self.velocity = 0

    @property
    def velocity(self):
        """Signed value for the speed and direction of the motor. Must be
        between -max_speed and +max_speed."""
        return (
            (1 if (self._direction == Direction.Forward) else -1)
            * self._speed
        )

    @velocity.setter
    def velocity(self, new):
        new_speed = abs(new)
        if new_speed > self._max_speed:
            raise ValueError(
                f'Velocity must be between -{self._max_speed} and '
                f'{self._max_speed}.'
            )
        if new < 0:
            self.direction = Direction.Backward
        else:
            self.direction = Direction.Forward
        self.speed = new_speed

    @property
    def speed(self):
        """Positive value for the speed of the motor. Must be between 0 and
        max_speed."""
        return self._speed

    @speed.setter
    def speed(self, new):
        if new < 0 or self._max_speed < new:
            raise ValueError(f'Speed must be between 0 and {self._max_speed}.')
        self._set_speed(new)
        self._speed = new

    @property
    def direction(self):
        """Direction of the motor stored and returned as an Enum. Can be set
        with a string. Only the first letter is considered, for example 'F',
        'b', 'foward', 'Back', and 'backwards' all work."""
        return self._direction

    @direction.setter
    def direction(self, new):
        if isinstance(new, str):
            new_first_char = new.lower()[0]
            if new_first_char == 'f':
                new = Direction.Forward
            elif new_first_char == 'b':
                new = Direction.Backward
        elif not isinstance(new, Direction):
            raise TypeError(
                f'new must be a string or Direction, not {type(new)}.'
            )
        self._set_direction(new)
        self._direction = new

    @abstractmethod
    def _set_speed(self, new):
        pass

    @abstractmethod
    def _set_direction(self, new):
        pass
