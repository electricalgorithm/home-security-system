"""
The Camera strategy for eye strategies.
"""
import logging
from datetime import datetime

import cv2
import numpy

from core.strategies.eye.base_eye_strategy import BaseEyeStrategy
from core.utils.datatypes import EyeStrategyResult

# Add logging support.
logger = logging.getLogger(__name__)


class CameraStrategy(BaseEyeStrategy):
    """
    The camera strategy for eye strategies.
    """
    def __init__(self, camera_id: int = 0):
        self._camera = cv2.VideoCapture(camera_id)
        if not self._camera.isOpened():
            raise RuntimeError('Could not start camera.')
    
    def check_if_detected(self) -> EyeStrategyResult:
        """This method checks if there are any protectors around."""
        # Get the frame from the camera.
        frame = self._get_frame()
        # Detect humans in the frame.
        regions, num_detections = self._detect_humans(frame)
        # Outline the regions in the frame.
        self._outline_the_regions(frame, regions)
        # Save the frame to the disk.
        self._save_frame(frame)
        # If there is a human in the frame, return True.
        if len(num_detections) > 0:
            return EyeStrategyResult(image=frame, result=True)
        return EyeStrategyResult(image=frame, result=False)

    # Internal methods.
    def _get_frame(self) -> numpy.ndarray:
        """This method returns the frame from the camera."""
        # Read the frame from the camera.
        _, frame = self._camera.read()
        return frame

    def _detect_humans(self, frame: numpy.ndarray) -> tuple[list[tuple[int, int, int, int]], float]:
        """This method checks if there is a person in front of the camera."""
        # Detect humans in the frame.
        hog_detector = cv2.HOGDescriptor()
        hog_detector.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        regions, num_detections = hog_detector.detectMultiScale(
            frame,
            winStride=(4, 4),
            padding=(4, 4),
            scale=1.05
        )
        logger.debug("Number of detections: " + str(num_detections)
                    + " Regions: " + str(regions))
        return regions, num_detections
    
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
