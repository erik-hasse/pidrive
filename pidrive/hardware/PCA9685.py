"""PCA9685 PWM controller"""
import time

from pidrive.abstract import Pin, PWMBoard

_MODE1_MASKS = {
    name: 1 << i for i, name in enumerate([
        'allcall', 'sub3', 'sub2', 'sub1', 'sleep', 'ai', 'extclk', 'restart'
    ])
}

_MODE2_MASKS = {
    name: 1 << i for i, name in enumerate([
        'outne0', 'outne1', 'outdrv', 'och', 'invrt'
    ])
}

_CHANNELS = {
    **{name: i for i, name in enumerate([
        'mode1', 'mode2', 'subadr1', 'subadr2', 'subadr3', 'allcalladr'
    ])},
    **{name: 0xFA + i for i, name in enumerate([
        'all_led_on_l', 'all_led_on_h', 'all_led_off_l', 'all_led_off_h',
        'prescale', 'testmode'
    ])}
}


def _not(x, n_bits=8):
    # Bitwise not with n_bits
    return (1 << n_bits) - 1 - x


class PCA9685_Pin(Pin):
    """A pin on the PCA9685 PWM control board. Change its on time by setting
    duty_cycle.

    Args:
        board (PCA9685): The board that the pin is on.
        pin_number (int): The pin number on the board.
        duty_cycle_res (int): The apparent resolution of the pin in software


    """
    _FIRST_LED_CHANNEL = 0x06
    PIN_RESOLUTION = 0x1000

    def __init__(self, board, pin_number, duty_cycle_res):
        self._board = board
        self._start_delay = int(
            pin_number * self.PIN_RESOLUTION / board.N_PINS
        )
        self._on_register = self._FIRST_LED_CHANNEL + 4 * pin_number
        self._off_register = self._on_register + 2
        self._set_register(self._on_register, self._start_delay)
        super().__init__(pin_number, self.PIN_RESOLUTION, duty_cycle_res)

    def _set_duty_cycle(self, new):
        # Handle the all-on case separately
        if new == self.PIN_RESOLUTION:
            self._set_register(
                self._on_register, new
            )
        else:
            self._set_register(
                self._on_register, self._start_delay
            )
            self._set_register(
                self._off_register,
                (self._start_delay + new) % self.PIN_RESOLUTION
            )

    def _set_register(self, register, value):
        # Set the 2 byte register to value
        if (value < 0 or self.PIN_RESOLUTION < value):
            raise ValueError(
                f'Pin must be be between 0 and {self.PIN_RESOLUTION}'
            )
        bytes_to_write = [value & 0xFF, value >> 8]
        for i, x in enumerate(bytes_to_write):
            # SMBus has a write_block, but it doesn't work as expected.
            self._board._bus.write_byte_data(
                self._board.address, register + i, x
            )


class PCA9685(PWMBoard):
    """A PCA9685 board.

    Args:
        bus (SMBus): The bus used to connect to the board.
        duty_cycle_res (int): The apparent resolution of the pins in software.
            This can be configured per pin after initialization.
        frequency (int): The frequency of the PWM in Hertz.
        jumper_address (int): The address soldered onto the board.

    """
    _BASE_ADDRESS = 0x40
    N_PINS = 16

    def __init__(
            self, bus, duty_cycle_res=4, frequency=60, jumper_address=0
    ):
        self._bus = bus
        self._address = self._BASE_ADDRESS + jumper_address
        self.frequency = frequency
        self._bus.write_byte_data(
            self.address, _CHANNELS['mode1'], _MODE1_MASKS['allcall']
        )
        self._bus.write_byte_data(
            self.address, _CHANNELS['mode2'], _MODE2_MASKS['outdrv']
        )
        super().__init__(
            [PCA9685_Pin(self, i, duty_cycle_res) for i in range(self.N_PINS)]
        )

    @property
    def address(self):
        """The actual I2C address of the board (0x40 + jumper_address)."""
        return self._address

    @property
    def frequency(self):
        """The frequency of the board in Hertz."""
        return self._frequency

    @frequency.setter
    def frequency(self, new):
        # get the old mode, but don't write 1 to the restart bit
        mode = self._bus.read_byte_data(
            self.address, _CHANNELS['mode1']
        ) & _not(_MODE1_MASKS['restart'])
        # sleep the PWM chip
        self._bus.write_byte_data(
            self.address, _CHANNELS['mode1'], mode | _MODE1_MASKS['sleep']
        )
        # Write the prescale
        prescale = round(25e6 / (4096 * new)) - 1
        self._bus.write_byte_data(
            self.address, _CHANNELS['prescale'], prescale
        )
        # Clear the sleep and wait 500 us
        mode &= _not(_MODE1_MASKS['sleep'])
        self._bus.write_byte_data(self.address, _CHANNELS['mode1'], mode)
        time.sleep(0.0005)
        # Set the restart flag
        self._bus.write_byte_data(
            self.address, _CHANNELS['mode1'], mode | _MODE1_MASKS['restart']
        )
        self._frequency = new
