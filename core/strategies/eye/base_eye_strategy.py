"""
The base strategy for eye strategies.
This strategy is used to define the interface for all eye strategies.
"""
from abc import abstractmethod, ABCMeta
from numpy import ndarray
from core.utils.datatypes import EyeStrategyResult
from core.strategies.detectors.base_detector_strategy import BaseDetectorStrategy, DetectorResult


class BaseEyeStrategy(metaclass=ABCMeta):
    """
    The base strategy for eye strategies.
    """
    @abstractmethod
    def set_detector(self, detector: BaseDetectorStrategy) -> None:
        """This method sets the detector strategy."""

    @abstractmethod
    def get_detector(self) -> BaseDetectorStrategy: 
        """This method returns the detector strategy."""

    @abstractmethod
    def check_if_detected(self) -> EyeStrategyResult:
        """This method checks if there are any protectors around."""

    def _detect_humans(self, frame: ndarray) -> DetectorResult:
        """This method checks if there is a person in front of the camera."""
        return self.get_detector().detect_humans(frame)

