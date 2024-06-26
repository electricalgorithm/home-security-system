"""
The observer for Home Security System.
"""
from core.observers.observer.base_observer import BaseObserver
from core.observers.subject.base_subject import BaseSubject
from core.observers.subject.eye_subject import EyeSubject
from core.observers.subject.wifi_subject import WiFiSubject
from core.strategies.notifier.base_notifier_strategy import BaseNotifierStrategy
from core.strategies.notifier.telegram_strategy import TelegramStrategy
from core.strategies.notifier.whatsapp_strategy import WhatsappStrategy
from core.utils.datatypes import EyeStates, WiFiStates
from core.utils.fileio_adaptor import read_latest_file, upload_to_fileio
from core.utils.logger import get_logger

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
            if isinstance(self._notifier, WhatsappStrategy):
                fileio_link = upload_to_fileio(
                    read_latest_file("~/.home-security-system/images")
                )
                self._notifier.notify_all(
                    f"There is an intruder! Here is the image: {fileio_link}."
                )
            elif isinstance(self._notifier, TelegramStrategy):
                latest_file = read_latest_file("~/.home-security-system/images")
                with open(latest_file, 'rb') as intruder_image:
                    self._notifier.notify_all("There is an intruder! Here is the image:")
                    self._notifier.send_image_all(intruder_image)
            else:
                logger.error("Notifier is not set!")

    def set_notifier(self, notifier: BaseNotifierStrategy) -> None:
        """This method is called when the observer is updated."""
        self._notifier = notifier
