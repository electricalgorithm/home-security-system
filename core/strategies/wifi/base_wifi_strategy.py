"""
The base strategy for WiFi strategies.
This strategy is used to define the interface for all WiFi strategies.
"""
from abc import abstractmethod, ABCMeta
from core.utils.datatypes import Protector, WiFiStrategyResult


class BaseWiFiStrategy(metaclass=ABCMeta):
    """
    The base strategy for WiFi strategies.
    """
    def __init__(self):
        self.protectors: list[Protector] = []

    def add_protector(self, protector: Protector | list[Protector]) -> None:
        """This method adds a protector to the list of protectors."""
        if isinstance(protector, list):
            self.protectors.extend(protector)
        else:
            self.protectors.append(protector)

    def remove_protector(self, protector: Protector | list[Protector]) -> None:
        """This method removes a protector from the list of protectors."""
        if isinstance(protector, list):
            for p in protector:
                self.protectors.remove(p)
        else:
            self.protectors.remove(protector)

    @abstractmethod
    def check_protectors(self) -> WiFiStrategyResult:
        """This method checks if there are any protectors around."""
