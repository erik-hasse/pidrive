try:
    from gpiozero import DigitalOutputDevice
except ImportError:
    DigitalOutputDevice = None
try:
    from smbus2 import SMBus
except ImportError:
    try:
        from smbus import SMBus
    except ImportError:
        SMBus = None

from pidrive.abstract import Car
from pidrive.hardware import PCA9685, TB6612Motor, PWMServo, USBWebcam


class PiCarV(Car):
    def __init__(self):
        if SMBus is None or DigitalOutputDevice is None:
            raise ImportError(
                'This module requires gpiozero and one of smbus or smbus2'
            )
        bus = SMBus(1)
        pwm = PCA9685(bus)
        pwm.pin(4).duty_cycle_res = 4
        pwm.pin(5).duty_cycle_res = 4
        drive_motors = [
            TB6612Motor(DigitalOutputDevice(17), pwm.pin(5)),
            TB6612Motor(DigitalOutputDevice(27), pwm.pin(4)),
        ]
        turning_motors = [
            PWMServo(pwm.pin(0), min_limit=-60, max_limit=60)
        ]
        camera = USBWebcam(
            pan=PWMServo(pwm.pin(1), min_pulse=2.5, max_pulse=0.5),
            tilt=PWMServo(pwm.pin(2), angle=-8, min_limit=-10)
        )
        super().__init__(drive_motors, turning_motors, camera=camera)
