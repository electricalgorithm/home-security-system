"""
The observer for Home Security System.
"""
import logging
from core.observers.observer.base_observer import BaseObserver
from core.observers.subject.base_subject import BaseSubject
from core.observers.subject.wifi_subject import WiFiSubject
from core.observers.subject.eye_subject import EyeSubject
from core.utils.datatypes import EyeStates, WiFiStates
from core.strategies.notifier.base_notifier_strategy import BaseNotifierStrategy

# Add logging support.
logger = logging.getLogger(__name__)


class HomeSecuritySystemObserver(BaseObserver):
    """
    The observer for Home Security System.
    """
    def __init__(self):
        self.wifi_state: WiFiStates = WiFiSubject.get_default_state()
        self.eye_state: EyeStates = EyeSubject.get_default_state()
        self._notifier: BaseNotifierStrategy = None

    def update(self, subject: BaseSubject) -> None:
        """This method is called when the observer is updated."""
        if isinstance(subject, WiFiSubject):
            self.wifi_state = subject.get_state()
            logger.debug("WiFi state: " + str(self.wifi_state.name))
        
        if isinstance(subject, EyeSubject):
            self.eye_state = subject.get_state()
            logger.debug("Eye state: " + str(self.eye_state.name))

        if self.wifi_state == WiFiStates.DISCONNECTED and self.eye_state == EyeStates.DETECTED:
            logger.info("There is an intruder!")
            self._notifier.notify_all("There is an intruder!")
        
    def set_notifier(self, notifier: BaseNotifierStrategy) -> None:
        """This method is called when the observer is updated."""
        self._notifier = notifier
