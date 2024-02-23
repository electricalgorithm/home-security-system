"""
This class inherits from IBaseSubject.
Concretes a subject WiFi features.
"""
from threading import Thread, Lock
from time import sleep

from core.utils.logger import get_logger
from core.utils.datatypes import WiFiStates
from core.observers.subject.base_subject import BaseSubject
from core.strategies.wifi.base_wifi_strategy import BaseWiFiStrategy

# Add logging support.
logger = get_logger(__name__)


class WiFiSubject(BaseSubject):
    """
    This class inherits from IBaseSubject.
    Concretes a subject for WiFiS features.
    """
    SINGLETON_LOCK: Lock | None = None
    CHECK_INTERVAL: int = 5

    @staticmethod
    def get_default_state() -> WiFiStates:
        """This method is called when the observer is updated."""
        return WiFiStates.UNREACHABLE

    def run(self, wifi_strategy: BaseWiFiStrategy) -> None:
        """This method is called when the observer is updated."""
        thread = Thread(target=self._run_in_loop, args=(wifi_strategy,))
        thread.start()
        logger.debug("WiFiSubject is running...")

    @classmethod
    def get_protector_lock(cls) -> Lock:
        """This method returns a Lock object where it can be
        used to block camera when there is a WiFi connection
        from protectors.
        """
        if cls.SINGLETON_LOCK is None:
            cls.SINGLETON_LOCK = Lock()
        return cls.SINGLETON_LOCK

    def _run_in_loop(self, wifi_strategy: BaseWiFiStrategy) -> None:
        """This method is called when the observer is updated."""
        protector_lock: Lock = self.get_protector_lock()

        while True:
            protectors = wifi_strategy.check_protectors()
            logger.debug("Protectors: %s %s", str(protectors.result), str(protectors.protector))

            if protectors.result:
                self.set_state(WiFiStates.CONNECTED)
                if not protector_lock.locked():
                    protector_lock.acquire()
            else:
                self.set_state(WiFiStates.DISCONNECTED)
                if protector_lock.locked():
                    protector_lock.release()
            sleep(self.CHECK_INTERVAL)
