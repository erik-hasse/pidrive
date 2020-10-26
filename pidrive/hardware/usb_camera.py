try:
    import cv2
except ImportError:
    cv2 = None

from pidrive.abstract import Sensor


class USBWebcam(Sensor):
    def __init__(self, camera_id=-1, pan=None, tilt=None):
        if cv2 is None:
            raise ImportError('This module requires opencv')
        self._cam = cv2.VideoCapture(camera_id)
        self._cam.set(cv2.CAP_PROP_BUFFER_SIZE, 1)
        super().__init__(pan=pan, tilt=tilt)

    def read(self):
        ret, frame = self._cam.read()
        ret, frame = self._cam.read()

        return frame
