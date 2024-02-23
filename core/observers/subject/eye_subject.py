"""
This class inherits from IBaseSubject.
Concretes a subject for Eye/Camera features.
"""
import os
from datetime import datetime
from time import sleep
from threading import Thread, Lock

import cv2

from core.utils.logger import get_logger
from core.utils.datatypes import EyeStates, EyeStrategyResult
from core.observers.subject.base_subject import BaseSubject
from core.strategies.eye.base_eye_strategy import BaseEyeStrategy

# Add logging support.
logger = get_logger(__name__)


class EyeSubject(BaseSubject):
    """
    This class inherits from IBaseSubject.
    Concretes a subject for Eye/Camera features.
    """
    DEFAULT_IMAGE_LOCATIONS: str = "~/.home-security-system/images"
    DEFAULT_SLEEP_INTERVAL = 10
    SLEEP_INTERVAL_DETECTED = 2

    def __init__(self, image_path: str = DEFAULT_IMAGE_LOCATIONS):
        super().__init__()
        self._image_path = (
            image_path
            if '~' not in image_path
            else os.path.expanduser(image_path)
        )

        # Create the default image directory if not exists.
        os.makedirs(self._image_path, exist_ok=True)

    @staticmethod
    def get_default_state() -> EyeStates:
        """This method is called when the observer is updated."""
        return EyeStates.UNREACHABLE

    def run(self,
            eye_strategy: BaseEyeStrategy,
            wifi_lock: Lock | None = None
            ) -> None:
        """This method is called when the observer is updated."""
        thread = Thread(target=self._run_in_loop, args=(self, eye_strategy, wifi_lock))
        thread.start()
        logger.debug("EyeSubject is running...")

    def _run_in_loop(self,
                     eye_strategy: BaseEyeStrategy,
                     wifi_lock: Lock | None = None
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
                logger.debug("EyeStrategyResult: %s", str(result.result))

                if result.result:
                    logger.debug("Changing state to DETECTED...")
                    self._save_image(result)
                    self.set_state(EyeStates.DETECTED)
                    sleep_interval = EyeSubject.SLEEP_INTERVAL_DETECTED
                else:
                    logger.debug("Changing state to NOT_DETECTED...")
                    self.set_state(EyeStates.NOT_DETECTED)
                    sleep_interval = EyeSubject.DEFAULT_SLEEP_INTERVAL

            #  If the WiFi subject does not give rights,
            # aka: "There is protectors around the house."
            else:
                logger.debug("Changing state to UNREACHABLE...")
                self.set_state(EyeStates.UNREACHABLE)
                sleep_interval = EyeSubject.DEFAULT_SLEEP_INTERVAL

            sleep(sleep_interval)

    def _save_image(self, result: EyeStrategyResult) -> None:
        """This method is called when the observer is updated."""
        logger.debug("Saving image to the disk...")
        time_now = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        file_location = f"{self._image_path}/intruder_{time_now}.jpg"
        cv2.imwrite(file_location, result.image)
        logger.debug("Image saved to the disk with name: intruder_%s.jpg", time_now)
