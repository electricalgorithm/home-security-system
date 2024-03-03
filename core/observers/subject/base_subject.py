"""
The base subject for observer pattern.
This observer is used to create subjects.
"""
from abc import ABCMeta, abstractmethod

from core.observers.observer.base_observer import BaseObserver
from core.utils.datatypes import ObserverStates
from core.utils.logger import get_logger

# Create a logger instance.
logger = get_logger(__name__)


class BaseSubject(metaclass=ABCMeta):
    """
    The base subject.
    This observer is used to create subjects.
    """
    def __init__(self):
        self._observers: list[BaseObserver] = []
        self._current_state: ObserverStates = self.get_default_state()

    def attach(self, observer: BaseObserver) -> None:
        """This method is called when the observer is updated."""
        self._observers.append(observer)

    def detach(self, observer: BaseObserver) -> None:
        """This method is called when the observer is updated."""
        self._observers.remove(observer)

    def notify(self) -> None:
        """This method is called when the observer is updated."""
        logger.debug("[Subject: %s] Notifying observers...",
                     self.__class__.__name__)
        for observer in self._observers:
            observer.update(self)

    def get_state(self) -> ObserverStates:
        """This method is called when the observer is updated."""
        return self._current_state

    def set_state(self, state: ObserverStates) -> None:
        """This method is called when the observer is updated."""
        logger.debug("[Subject: %s] %s->%s",
                     self.__class__.__name__,
                     self._current_state.name,
                     state.name)
        self._current_state = state
        self.notify()

    @abstractmethod
    @staticmethod
    def get_default_state() -> ObserverStates:
        """This method is called when the observer is updated."""
        raise NotImplementedError

    @abstractmethod
    def run(self) -> None:
        """This method is called when the observer is updated."""
        raise NotImplementedError
