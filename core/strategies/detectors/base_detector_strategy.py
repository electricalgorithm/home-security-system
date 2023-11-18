"""
The base strategy for detector strategies.
This strategy is used to define the interface for all detector strategies.
"""

from abc import abstractmethod, ABCMeta
from dataclasses import dataclass

import numpy


@dataclass
class DetectorResult:
    """This class represents the result of a detector strategy."""
    image: numpy.ndarray
    human_found: bool
    regions: list[tuple[int, int, int, int]] = None
    num_detections: float = None


class BaseDetectorStrategy(metaclass=ABCMeta):
    """
    The base strategy for detector strategies.
    """
    @staticmethod
    @abstractmethod
    def detect_humans(frame: numpy.ndarray) -> DetectorResult:
        """This method detects if there are any humans in the frame."""
