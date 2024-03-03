"""
This class inherits from IBaseSubject.
Concretes a subject WiFi features.
"""
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from time import sleep

from core.observers.subject.base_subject import BaseSubject
from core.strategies.wifi.base_wifi_strategy import BaseWiFiStrategy
from core.utils.datatypes import WiFiStates
from core.utils.logger import get_logger

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

    def _cb_save(self, future) -> None:
        """This method is called when the observer is updated."""
        logger.warning("[WiFiSubject] The thread died.")
        file_location = "wifisubject_thread_died.txt"
        with open(file_location, "w", encoding="utf-8") as file:
            file.write("The thread died.")
        logger.warning("[WiFiSubject] The thread died. A file is created at %s.",
                       file_location)

    def run(self, wifi_strategy: BaseWiFiStrategy) -> None:
        """This method is called when the observer is updated."""
        thread = ThreadPoolExecutor(
            max_workers=1,
            thread_name_prefix="wifisubject"
        ).submit(self._run_in_loop, self, wifi_strategy)
        thread.add_done_callback(self._cb_save)

    @classmethod
    def get_protector_lock(cls) -> Lock:
        """This method returns a Lock object where it can be
        used to block camera when there is a WiFi connection
        from protectors.
        """
        if cls.SINGLETON_LOCK is None:
            cls.SINGLETON_LOCK = Lock()
        return cls.SINGLETON_LOCK

    @staticmethod
    def _run_in_loop(self, wifi_strategy: BaseWiFiStrategy) -> None:
        """This method is called when the observer is updated."""
        logger.debug("[WiFiSubject] Thread is started.")

        protector_lock: Lock = self.get_protector_lock()

        while True:
            protectors = wifi_strategy.check_protectors()
            logger.debug("[WiFiSubject] Protectors: %s %s",
                         str(protectors.result),
                         str(protectors.protector))

            if protectors.result:
                self.set_state(WiFiStates.CONNECTED)
                if not protector_lock.locked():
                    protector_lock.acquire()
                    logger.debug("[WiFiSubject] Protector lock is acquired.")
            else:
                self.set_state(WiFiStates.DISCONNECTED)
                if protector_lock.locked():
                    protector_lock.release()
                    logger.debug("[WiFiSubject] Protector lock is released.")
            sleep(self.CHECK_INTERVAL)
