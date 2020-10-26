from abc import ABC, abstractmethod

class Sensor(ABC):
    def __init__(self, pan=None, tilt=None):
        self.pan = pan
        self.tilt = tilt

    def up(self, amount=10):
        try:
            self.tilt.angle += amount
        except AttributeError as e:
            raise AttributeError(
                f'Tilt motor {self.tilt} does not support angle assignment'
            ) from e
        except ValueError:
            pass

    def down(self, amount=10):
        try:
            self.tilt.angle -= amount
        except AttributeError as e:
            raise AttributeError(
                f'Tilt motor {self.tilt} does not support angle assignment'
            ) from e
        except ValueError:
            pass

    def left(self, amount=10):
        try:
            self.pan.angle -= amount
        except AttributeError as e:
            raise AttributeError(
                f'Pan motor {self.pan} does not support angle assignment'
            ) from e
        except ValueError:
            pass

    def right(self, amount=10):
        try:
            self.pan.angle += amount
        except AttributeError as e:
            raise AttributeError(
                f'Pan motor {self.pan} does not support angle assignment'
            ) from e
        except ValueError:
            pass
