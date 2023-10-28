"""
This module contains the ObserverEye class.
"""
import cv2
import numpy


class ObserverEye:
    """This class is a namespace for all the operations related to eye observation."""

    def __init__(self):
        """This method initializes the ObserverEye class."""
        # Get the video capture object.
        self._camera = cv2.VideoCapture(0)
        if not self._camera.isOpened():
            raise RuntimeError('Could not start camera.')

    def get_frame(self) -> numpy.ndarray:
        """This method returns the frame from the camera."""
        # Read the frame from the camera.
        _, frame = self._camera.read()
        return frame

    def detect_humans(self) -> bool:
        """This method checks if there is a person in front of the camera."""
        # Get the frame from the camera.
        frame = self.get_frame()

        # Detect humans in the frame.
        hog_detector = cv2.HOGDescriptor()
        hog_detector.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        regions, num_detections = hog_detector.detectMultiScale(
            frame,
            winStride=(4, 4),
            padding=(4, 4),
            scale=1.05
        )

        for (x, y, w, h) in regions:
            cv2.rectangle(frame, (x, y),  (x + w, y + h),  (0, 0, 255), 2)

        # Showing the output Image
        cv2.imshow("Image", frame)
        cv2.waitKey(0)

        cv2.destroyAllWindows()

        # If there is a face in the frame, return True.
        if len(num_detections) > 0:
            return True
        return False
