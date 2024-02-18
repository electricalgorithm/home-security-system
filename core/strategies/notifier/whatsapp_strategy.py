"""
This module contains the Whatsapp notifier strategy.
"""
import logging

import requests

from core.utils.datatypes import WhatsappReciever
from core.strategies.notifier.base_notifier_strategy import BaseNotifierStrategy

# Get the logger instance.
logger = logging.getLogger(__name__)


class WhatsappStrategy(BaseNotifierStrategy):
    """
    The Whatsapp notifier strategy.
    """
    API_URL = "https://api.callmebot.com/whatsapp.php"

    def notify_all(self, message: str) -> None:
        """This method is called when the notifier is updated."""
        for reciever in self._recievers:
            if isinstance(reciever, WhatsappReciever):
                self._send_message(reciever, message)

    def _send_message(self, reciever: WhatsappReciever, message: str) -> bool:
        """Send a WhatsApp message to the user."""
        logger.debug("Sending WhatsApp message (%s) to %s", message, reciever.telephone_number)
        # Send the request.
        request_url = f"{self.API_URL}?phone={reciever.telephone_number}&text={message}&apikey={reciever.api_key}"
        response = requests.get(request_url, timeout=10)

        # Check if the request was unsuccessful.
        if response.status_code != 200 or "ERROR" in response.text:
            logger.error("Failed to send WhatsApp message to %s", reciever.telephone_number)
            logger.error("Status code: %s", response.status_code)
            return False

        # Log the success.
        logger.info("WhatsApp message (%s) sent to %s", message, reciever.telephone_number)
        return True
