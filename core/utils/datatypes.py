"""
This module contains datatypes needed for architecture.
"""
from dataclasses import dataclass
from enum import IntEnum, auto, unique


@dataclass
class Protector:
    """This class represents a protector."""
    name: str
    address: str


@dataclass
class WiFiStrategyResult:
    """This class represents a strategy result."""
    protector: Protector
    result: bool


@dataclass
class EyeStrategyResult:
    """This class represents a strategy result."""
    image: object
    result: bool


@dataclass
class ConnectedDeviceResult:
    """This class represents a result."""
    address: str


@unique
class ObserverStates(IntEnum):
    """This class represents a state."""


@unique
class WiFiStates(ObserverStates):
    """This class represents a state."""
    UNREACHABLE = auto()
    CONNECTED = auto()
    DISCONNECTED = auto()


@unique
class EyeStates(ObserverStates):
    """This class represents a state."""
    UNREACHABLE = auto()
    DETECTED = auto()
    NOT_DETECTED = auto()


@dataclass
class NotifierReciever:
    """This class represents a notifier reciever."""
    name: str


@dataclass
class WhatsappReciever(NotifierReciever):
    """This class represents WhatsApp reciever."""
    telephone_number: str
    api_key: str


@dataclass
class TelegramReciever(NotifierReciever):
    """This class represents Telegram reciever."""
    chat_id: str
