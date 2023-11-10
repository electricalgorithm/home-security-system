"""
This module contains the Whatsapp notifier strategy.
"""
from core.utils.datatypes import WhatsappReciever
from core.strategies.notifier.base_notifier_strategy import BaseNotifierStrategy


class WhatsappStrategy(BaseNotifierStrategy):
    """
    The Whatsapp notifier strategy.
    """
    def notify_all(self, message: str) -> None:
        """This method is called when the notifier is updated."""
        for reciever in self._recievers:
            if isinstance(reciever, WhatsappReciever):
                print(f"Sending message: {message} to {reciever.name} with telephone number {reciever.telephone_number}.")