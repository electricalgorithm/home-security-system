"""
The HOG descriptor strategy for detector strategies.
"""
import cv2
import numpy
from base_detector_strategy import BaseDetectorStrategy, DetectorResult


class HogDescriptorStrategy(BaseDetectorStrategy):
    """
    The HOG descriptor strategy for detector strategies.
    """
    @staticmethod
    def detect_humans(frame: numpy.ndarray) -> DetectorResult:
        """This method detects if there are any humans in the frame."""
        # Detect humans in the frame.
        hog_detector = cv2.HOGDescriptor()
        hog_detector.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        regions, num_detections = hog_detector.detectMultiScale(
            grey,
            winStride=(2, 2),
            padding=(4, 4),
            scale=1.03,
        )

        result = DetectorResult(
            image=frame,
            human_found=len(num_detections) > 0,
            regions=regions,
            num_detections=num_detections,
        )
        return result
