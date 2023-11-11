"""
This class inherits from IBaseSubject.
Concretes a subject WiFi features.
"""
import logging
from threading import Thread
from time import sleep

from core.utils.datatypes import WiFiStates
from core.observers.subject.base_subject import BaseSubject
from core.strategies.wifi.base_wifi_strategy import BaseWiFiStrategy

# Add logging support.
logger = logging.getLogger(__name__)


class WiFiSubject(BaseSubject):
    """
    This class inherits from IBaseSubject.
    Concretes a subject for WiFiS features.
    """
    @staticmethod
    def get_default_state() -> WiFiStates:
        """This method is called when the observer is updated."""
        return WiFiStates.UNREACHABLE

    def run(self, wifi_strategy: BaseWiFiStrategy) -> None:
        """This method is called when the observer is updated."""
        thread = Thread(target=self._run_in_loop, args=(self, wifi_strategy,))
        thread.start()
        logger.debug("WiFiSubject is running...")

    @staticmethod
    def _run_in_loop(self, wifi_strategy: BaseWiFiStrategy) -> None:
        """This method is called when the observer is updated."""
        while True:
            protectors = wifi_strategy.check_protectors()
            logger.debug("Protectors: " + str(protectors.result) + " " + str(protectors.protector))

            if protectors.result:
                self.set_state(WiFiStates.CONNECTED)
            else:
                self.set_state(WiFiStates.DISCONNECTED)
            sleep(5)
