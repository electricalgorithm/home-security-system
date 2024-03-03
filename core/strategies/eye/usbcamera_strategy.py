"""
The Camera strategy for eye strategies.
"""
import cv2
import numpy

from core.strategies.detectors.base_detector_strategy import BaseDetectorStrategy
from core.strategies.eye.base_eye_strategy import BaseEyeStrategy
from core.utils.logger import get_logger

# Add logging support.
logger = get_logger(__name__)


class UsbCameraStrategy(BaseEyeStrategy):
    """
    The camera strategy for eye strategies.
    """
    def __init__(self, camera_id: int = 0):
        self._camera_id = camera_id
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
        # Create a camera object.
        camera = cv2.VideoCapture(self._camera_id)
        # Set the camera resolution.
        camera.set(3, 640)
        camera.set(4, 480)
        #  Read the frame from the camera.
        _, frame = camera.read()
        # Release the camera.
        camera.release()
        return frame
