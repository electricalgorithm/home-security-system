"""
The Camera strategy for eye strategies.
"""
import numpy
from picamera2 import Picamera2

from core.utils.logger import get_logger
from core.strategies.detectors.base_detector_strategy import BaseDetectorStrategy
from core.strategies.eye.base_eye_strategy import BaseEyeStrategy

# Add logging support.
logger = get_logger(__name__)


class PiCameraStrategy(BaseEyeStrategy):
    """
    The camera strategy for eye strategies.
    """
    def __init__(self):
        self._detector = None

    # Interface methods.
    def set_detector(self, detector: BaseDetectorStrategy) -> None:
        """This method sets the detector strategy."""
        self._detector = detector

    def get_detector(self) -> BaseDetectorStrategy:
        """This method returns the detector strategy."""
        return self._detector

    def get_frame(self) -> numpy.ndarray:
        """This method returns the frame from the camera."""
        # Internal attributes
        picam2 = Picamera2()
        picam2.configure(picam2.create_preview_configuration(
            main={"format": 'XRGB8888', "size": (640, 480)}
        ))
        picam2.start()
        frame = picam2.capture_array()
        picam2.close()
        del picam2
        return frame
