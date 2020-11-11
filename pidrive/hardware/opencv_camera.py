try:
    import cv2
except ImportError:
    cv2 = None

from pidrive.abstract.sensor import Sensor


class OpenCVCamera(Sensor):
    def __init__(self, camera_id=-1, pan=None, tilt=None, opencv_props=None):
        if cv2 is None:
            raise ImportError('This module requires opencv')

        self._cam = cv2.VideoCapture(camera_id)

        if opencv_props is not None:
            for k, v in opencv_props.items():
                self._cam.set(getattr(cv2, k), v)

        self._buffer_size = self._cam.get(cv2.CAP_PROP_BUFFERSIZE)
        super().__init__(pan=pan, tilt=tilt)

    def read(self):
        for _ in range(self._buffer_size):
            self._cam.grab()

        return self._cam.retrieve()[1]
