"""
This module contains the base notifier strategy.
"""
from abc import ABCMeta, abstractmethod
from core.utils.datatypes import NotifierReciever


class BaseNotifierStrategy(metaclass=ABCMeta):
    """
    The base notifier strategy.
    This class is used to create notifier strategies.
    """
    def __init__(self) -> None:
        self._recievers: list[NotifierReciever] = []

    def add_reciever(self, reciever: NotifierReciever) -> None:
        """This method is called when a reciever is added."""
        self._recievers.append(reciever)

    @abstractmethod
    def notify_all(self, message: str) -> None:
        """This method is called when the notifier is updated."""
        raise NotImplementedError
