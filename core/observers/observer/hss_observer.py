"""
The observer for Home Security System.
"""
from core.utils.logger import get_logger
from core.observers.observer.base_observer import BaseObserver
from core.observers.subject.base_subject import BaseSubject
from core.observers.subject.wifi_subject import WiFiSubject
from core.observers.subject.eye_subject import EyeSubject
from core.utils.datatypes import EyeStates, WiFiStates
from core.utils.fileio_adaptor import upload_to_fileio, read_latest_file
from core.strategies.notifier.base_notifier_strategy import BaseNotifierStrategy

# Add logging support.
logger = get_logger(__name__)


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
            logger.debug("WiFi state: %s", str(self.wifi_state.name))

        if isinstance(subject, EyeSubject):
            self.eye_state = subject.get_state()
            logger.debug("Eye state: %s", str(self.eye_state.name))

        if self.wifi_state == WiFiStates.DISCONNECTED and self.eye_state == EyeStates.DETECTED:
            logger.info("There is an intruder!")
            fileio_link = upload_to_fileio(
                read_latest_file("~/.home-security-system/images")
            )
            self._notifier.notify_all(f"There is an intruder! Here is the image: {fileio_link}.")

    def set_notifier(self, notifier: BaseNotifierStrategy) -> None:
        """This method is called when the observer is updated."""
        self._notifier = notifier
