"""
The Camera strategy for eye strategies.
"""
import logging
from datetime import datetime

import cv2
import numpy

from core.strategies.detectors.base_detector_strategy import BaseDetectorStrategy, DetectorResult
from core.strategies.eye.base_eye_strategy import BaseEyeStrategy
from core.utils.datatypes import EyeStrategyResult

# Add logging support.
logger = logging.getLogger(__name__)


class CameraStrategy(BaseEyeStrategy):
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
    
    def check_if_detected(self) -> EyeStrategyResult:
        """This method checks if there are any protectors around."""
        # Get the frame from the camera.
        frame = self._get_frame()
        # Detect humans in the frame.
        result = self._detect_humans(frame)
        # Outline the regions in the frame.
        # self._outline_the_regions(frame, regions)
        # Save the frame to the disk.
        # self._save_frame(frame)
        # If there is a human in the frame, return True.
        if result.human_found:
            return EyeStrategyResult(image=frame, result=True)
        return EyeStrategyResult(image=frame, result=False)

    # Internal methods.
    def _get_frame(self) -> numpy.ndarray:
        """This method returns the frame from the camera."""
        # Create a camera object.
        camera = cv2.VideoCapture(self._camera_id)
        # Set the camera resolution.
        camera.set(3, 640)
        camera.set(4, 480)
        # Read the frame from the camera.
        _, frame = camera.read()
        # Release the camera.
        camera.release()
        return frame
    
    def _outline_the_regions(self, frame: numpy.ndarray, regions: list[tuple[int, int, int, int]]) -> None:
        """This method outlines the regions in the frame."""
        for (x, y, w, h) in regions:
            cv2.rectangle(frame, (x, y),  (x + w, y + h),  (0, 0, 255), 2)
 
    def _save_frame(self, frame: numpy.ndarray) -> None:
        """This method saves the frame to the disk."""
        # Get current date and time.
        current_date_time = datetime.now()
        # Save the frame.
        cv2.imwrite(f"frame_{current_date_time}.jpg", frame)
