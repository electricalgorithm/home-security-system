"""
This class inherits from IBaseSubject.
Concretes a subject for Eye/Camera features.
"""
from time import sleep
from threading import Thread
from core.utils.datatypes import EyeStates, EyeStrategyResult
from core.observers.subject.base_subject import BaseSubject
from core.strategies.eye.base_eye_strategy import BaseEyeStrategy


class EyeSubject(BaseSubject):
    """
    This class inherits from IBaseSubject.
    Concretes a subject for Eye/Camera features.
    """
    def __init__(self):
        super().__init__()
        self._result: EyeStrategyResult = None

    @staticmethod
    def get_default_state() -> EyeStates:
        """This method is called when the observer is updated."""
        return EyeStates.UNREACHABLE

    def run(self, eye_strategy: BaseEyeStrategy) -> None:
        """This method is called when the observer is updated."""
        thread = Thread(target=self._run_in_loop, args=(self, eye_strategy,))
        thread.start()

    def save_result(self, result: EyeStrategyResult) -> None:
        """This method is called when the observer is updated to DETECTED."""
        self._result = result

    @staticmethod
    def _run_in_loop(self, eye_strategy: BaseEyeStrategy) -> None:
        """This method is called when the observer is updated."""
        while True:
            result = eye_strategy.check_if_detected()
            print("Eye result: " + str(result.result))
            print("Eye state: " + str(self.get_state().name))
            if result.result:
                self.set_state(EyeStates.DETECTED)
                self.save_result(result)
            else:
                self.set_state(EyeStates.NOT_DETECTED)
            sleep(5)
        