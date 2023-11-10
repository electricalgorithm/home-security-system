"""
The Camera strategy for eye strategies.
"""
import cv2
import numpy
from core.strategies.eye.base_eye_strategy import BaseEyeStrategy
from core.utils.datatypes import EyeStrategyResult


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
        # frame = self._get_frame()
        # Detect humans in the frame.
        # result = self._detect_humans(frame)
        # return result
        return EyeStrategyResult(image=None, result=True)

    # Internal methods.
    def _get_frame(self) -> numpy.ndarray:
        """This method returns the frame from the camera."""
        # Read the frame from the camera.
        _, frame = self._camera.read()
        return frame

    def _detect_humans(self, frame: numpy.ndarray) -> EyeStrategyResult:
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

        # Draw rectangles around the detected humans.
        for (x, y, w, h) in regions:
            cv2.rectangle(frame, (x, y),  (x + w, y + h),  (0, 0, 255), 2)

        # Showing the output Image
        cv2.imshow("Image", frame)
        cv2.waitKey(0)

        cv2.destroyAllWindows()

        # If there is a face in the frame, return True.
        if len(num_detections) > 0:
            return EyeStrategyResult(image=frame, result=True)
        return EyeStrategyResult(image=frame, result=False)