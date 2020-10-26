from pidrive.abstract import Servo


class PWMServo(Servo):
    def __init__(
            self, pin, angle=0, min_angle=-90, max_angle=90,
            min_pulse=0.5, max_pulse=2.5, min_limit=None, max_limit=None
    ):
        self._pin = pin
        self._min_pulse = min_pulse
        self._max_pulse = max_pulse
        a2p_slope = (max_pulse - min_pulse) / (max_angle - min_angle)
        a2p_int = min_pulse - a2p_slope * min_angle
        self._angle_to_pulse = lambda a: a2p_slope * a + a2p_int
        super().__init__(min_angle, max_angle, angle, min_limit, max_limit)

    def _set_angle(self, new):
        cycle = self._pin.duty_cycle_res * (
            self._pin.board.frequency
            * self._angle_to_pulse(new)
            / 1000
        )
        self._pin.duty_cycle = cycle
