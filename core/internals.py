"""
This module contains Protector class.
"""

from dataclasses import dataclass

@dataclass
class Protector:
    """This class represents a protector."""

    name: str
    mac_addr: str
