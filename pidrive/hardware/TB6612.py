"""TB6612 Motor Controller"""
from pidrive.abstract import DriveMotor
from pidrive.types import Direction


class TB6612Motor(DriveMotor):
    """A motor controlled by the TB6612 board.

    Args:
        direction_pin (gpiozero.DigitalOutputPin): The GPIO pin connected to
            the direction control on the board.
        speed pin (picar.abstract.Pin): The PWM Pin connected to the speed
            control on the board.
        forward_high (bool): Used to configure the motor direction. If car is
            moving in the opposite direction, switch this.

    """
    def __init__(
            self, direction_pin, speed_pin,
            forward_high=True
    ):
        self._direction_pin = direction_pin
        self._speed_pin = speed_pin
        self._forward_high = forward_high
        super().__init__(speed_pin.duty_cycle_res)

    def _set_speed(self, new):
        self._speed_pin.duty_cycle = new

    def _set_direction(self, new):
        # TODO: Support RPi.GPIO pins too
        self._direction_pin.value = int(
            self._forward_high != (new == Direction.Forward)
        )
