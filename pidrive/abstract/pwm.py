from abc import ABC, abstractmethod
import warnings


class Pin(ABC):
    """An abstract class for a pin on a PWM board.

    The only method which must be implemented is _set_duty_cycle. This is
    called when duty_cycle is set. A value between 0 and pin_res (inclusive) is
    passed. The implementation should interact with the hardware to set the pin
    to the given value.

    Args:
        pin_number (int): The ID of this pin on the board.
        pin_res (int): The actual resolution of the pin in hardware.
        duty_cycle_res (int): The apparent resolution of the pin in software.

    """
    def __init__(self, pin_number, pin_res, duty_cycle_res):
        self._pin_number = pin_number
        self._pin_res = pin_res
        self.duty_cycle_res = duty_cycle_res
        self.duty_cycle = 0

    @property
    def duty_cycle_res(self):
        """The apparent resolution of the pin in software."""
        return self._duty_cycle_res

    @duty_cycle_res.setter
    def duty_cycle_res(self, new):
        if self._pin_res < new:
            raise ValueError(
                "duty_cycle_res must be less than or equal to pin_res."
            )
        if not (self._pin_res / new).is_integer():
            warnings.warn(
                "duty_cycle_res should be a divisor of pin_res. If it isn't, "
                'values will not be mapped exactly.'
            )
        self._duty_cycle_res = new

    @property
    def duty_cycle(self):
        """The current amount of time that the pin is high. Set this to change
        the PWM on time. Must be between 0 and duty_cycle_res, inclusive."""
        return self._duty_cycle * self.duty_cycle_res / self._pin_res

    @duty_cycle.setter
    def duty_cycle(self, new):
        if new < 0 or new > self.duty_cycle_res:
            raise ValueError(
                f'New value must be between 0 and {self.duty_cycle_res}'
            )
        new_duty_cycle = round(
            new * self._pin_res / self.duty_cycle_res
        )
        self._set_duty_cycle(new_duty_cycle)
        self._duty_cycle = new_duty_cycle

    @abstractmethod
    def _set_duty_cycle(self, new):
        pass


class PWMBoard(ABC):
    """A PWM board contains a list of instances of pins and a way to get each
    pin."""
    def __init__(self, pins):
        if not all(isinstance(x, Pin) for x in pins):
            raise ValueError('pins must be a list of Pin instances')
        self._pins = pins

    def pin(self, i):
        """Get pin i from this board."""
        return self._pins[i]
