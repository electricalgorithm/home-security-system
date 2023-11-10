"""
The base observer.
This observer is used to create observers.
"""
from abc import ABCMeta, abstractmethod


class BaseObserver(metaclass=ABCMeta):
    """
    The base observer.
    This observer is used to create observers.
    """

    @abstractmethod
    def update(self, subject) -> None:
        """This method is called when the observer is updated."""
        raise NotImplementedError
