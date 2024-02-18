"""
This class inherits from IBaseSubject.
Concretes a subject for Eye/Camera features.
"""
import logging
from datetime import datetime
from time import sleep
from threading import Thread, Lock
from typing import Optional

import cv2

from core.utils.datatypes import EyeStates, EyeStrategyResult
from core.observers.subject.base_subject import BaseSubject
from core.strategies.eye.base_eye_strategy import BaseEyeStrategy

# Add logging support.
logger = logging.getLogger(__name__)


class EyeSubject(BaseSubject):
    """
    This class inherits from IBaseSubject.
    Concretes a subject for Eye/Camera features.
    """
    DEFAULT_SLEEP_INTERVAL = 10
    SLEEP_INTERVAL_DETECTED = 5

    def __init__(self, image_path: str):
        super().__init__()
        self._image_path = image_path

    @staticmethod
    def get_default_state() -> EyeStates:
        """This method is called when the observer is updated."""
        return EyeStates.UNREACHABLE

    def run(self,
            eye_strategy: BaseEyeStrategy,
            wifi_lock: Optional[Lock] = None
            ) -> None:
        """This method is called when the observer is updated."""
        thread = Thread(target=self._run_in_loop, args=(self, eye_strategy, wifi_lock))
        thread.start()
        logger.debug("EyeSubject is running...")

    @staticmethod
    def _run_in_loop(self,
                     eye_strategy: BaseEyeStrategy,
                     wifi_lock: Optional[Lock] = None
                     ) -> None:
        """This method is called when the observer is updated."""
        sleep_interval = EyeSubject.DEFAULT_SLEEP_INTERVAL

        # Create a dummy lock instance if not given.
        if wifi_lock is None:
            wifi_lock = Lock()

        while True:
            # If WiFi subject would give rights to use camera,
            # Check if any intruders detected.
            if not wifi_lock.locked():
                result = eye_strategy.check_if_detected()
                logger.debug("EyeStrategyResult: " + str(result.result))

                if result.result:
                    self.set_state(EyeStates.DETECTED)
                    self._save_image(result)
                    sleep_interval = EyeSubject.SLEEP_INTERVAL_DETECTED
            
            # If the WiFi subject does not give rights,
            # aka: "There is protectors around the house."
            else:
                self.set_state(EyeStates.NOT_DETECTED)
                sleep_interval = EyeSubject.DEFAULT_SLEEP_INTERVAL

            sleep(sleep_interval)
    
    def _save_image(self, result: EyeStrategyResult) -> None:
        """This method is called when the observer is updated."""
        time_now = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        file_location = f"{self._image_path}/intruder_{time_now}.jpg"
        cv2.imwrite(file_location, result.image)
        logger.debug("Image saved to the disk with name: " + f"intruder_{time_now}.jpg")
        