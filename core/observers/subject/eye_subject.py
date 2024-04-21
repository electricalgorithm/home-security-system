"""
This class inherits from IBaseSubject.
Concretes a subject for Eye/Camera features.
"""
import os
from concurrent.futures import Future, ThreadPoolExecutor
from datetime import datetime
from threading import Lock
from time import sleep, time
from typing import Optional

import cv2

from core.observers.subject.base_subject import BaseSubject
from core.strategies.eye.base_eye_strategy import BaseEyeStrategy
from core.utils.datatypes import EyeStates, EyeStrategyResult
from core.utils.logger import get_logger

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

        # To run the eye after thread dies.
        self.thread: Optional[Future] = None
        self._eye_strategy: Optional[BaseEyeStrategy] = None
        self._wifi_lock: Optional[Lock] = None

        # Create the default image directory if not exists.
        os.makedirs(self._image_path, exist_ok=True)

    @staticmethod
    def get_default_state() -> EyeStates:
        """This method is called when the observer is updated."""
        return EyeStates.UNREACHABLE

    def run(self,
            eye_strategy: BaseEyeStrategy,
            wifi_lock: Optional[Lock] = None
            ) -> None:
        """This method is called when the observer is updated."""
        # Update the latest configurations.
        self._eye_strategy = eye_strategy
        self._wifi_lock = wifi_lock

        # Run the thread.
        self.thread = ThreadPoolExecutor(
            max_workers=1,
            thread_name_prefix="eyesubject"
        ).submit(self._run_in_loop, self, eye_strategy, wifi_lock)
        self.thread.add_done_callback(self._cb_done)

    @staticmethod
    def _run_in_loop(self,
                     eye_strategy: BaseEyeStrategy,
                     wifi_lock: Optional[Lock] = None
                     ) -> None:
        """This method is called when the observer is updated."""
        logger.debug("[EyeSubject] Thread is started.")
        sleep_interval = EyeSubject.DEFAULT_SLEEP_INTERVAL

        # Create a dummy lock instance if not given.
        if wifi_lock is None:
            logger.debug("[EyeSubject] A lock instance is generated.")
            wifi_lock = Lock()
            
        # Save an initial image.
        initial_frame = eye_strategy.get_frame()
        file_location = f"{self._image_path}/initial_frame.jpg"
        cv2.imwrite(file_location, initial_frame)
        logger.debug("[EyeSubject] Initial frame has been saved.")

        while True:
            # If WiFi subject would give rights to use camera,
            # Check if any intruders detected.
            logger.debug("[EyeSubject] WiFi Lock Status: %s", wifi_lock.locked())
            if not wifi_lock.locked():
                result = eye_strategy.check_if_detected()
                logger.debug("[EyeSubject] EyeStrategyResult: %s", str(result.result))

                if result.result:
                    logger.debug("[EyeSubject] Changing state to DETECTED...")
                    self._save_image(result)
                    self.set_state(EyeStates.DETECTED)
                    sleep_interval = EyeSubject.SLEEP_INTERVAL_DETECTED
                else:
                    logger.debug("[EyeSubject] Changing state to NOT_DETECTED...")
                    self.set_state(EyeStates.NOT_DETECTED)
                    sleep_interval = EyeSubject.DEFAULT_SLEEP_INTERVAL

            #  If the WiFi subject does not give rights,
            # aka: "There is protectors around the house."
            else:
                logger.debug("[EyeSubject] Changing state to UNREACHABLE...")
                self.set_state(EyeStates.UNREACHABLE)
                sleep_interval = EyeSubject.DEFAULT_SLEEP_INTERVAL

            sleep(sleep_interval)

    def _save_image(self, result: EyeStrategyResult) -> None:
        """This method is called when the observer is updated."""
        logger.debug("[EyeSubject] Saving image to the disk...")
        time_now = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        file_location = f"{self._image_path}/intruder_{time_now}.jpg"
        cv2.imwrite(file_location, result.image)
        logger.debug("[EyeSubject] Image saved to the disk with name: intruder_%s.jpg",
                     time_now)

    def _cb_done(self, future) -> None:
        """This method is called when the observer is updated."""
        logger.warning("[EyeSubject] The thread died.")

        # Start the thread again.
        self.run(self._eye_strategy, self._wifi_lock)
