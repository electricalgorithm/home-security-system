"""
The base strategy for eye strategies.
This strategy is used to define the interface for all eye strategies.
"""
from abc import abstractmethod, ABCMeta
from core.utils.datatypes import EyeStrategyResult


class BaseEyeStrategy(metaclass=ABCMeta):
    """
    The base strategy for eye strategies.
    """
    @abstractmethod
    def check_if_detected(self) -> EyeStrategyResult:
        """This method checks if there are any protectors around."""
