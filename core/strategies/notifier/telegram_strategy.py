"""
This module contains the Telegram notifier strategy.
"""
import telebot

from core.strategies.notifier.base_notifier_strategy import BaseNotifierStrategy
from core.utils.datatypes import TelegramReciever
from core.utils.logger import get_logger

# Get the logger instance.
logger = get_logger(__name__)


class TelegramStrategy(BaseNotifierStrategy):
    """
    The Telegram notifier strategy.
    """
    
    def __init__(self, api_key: str) -> 'TelegramStrategy':
        """Initilizes the Telegram modifier strategy."""
        self._bot = telebot.TeleBot(token=api_key,
                                    threaded=True,
                                    num_threads=2)
        super().__init__()
        
    def notify_all(self, message: str) -> None:
        """This method is called when the notifier is updated."""
        for reciever in self._recievers:
            if isinstance(reciever, TelegramReciever):
                logger.debug("Sending Telegram message (%s) to %s", message, reciever.chat_id)
                self._bot.send_message(reciever.chat_id, message)
    
    def send_image_all(self, image: bytes) -> None:
        """This method is called when the notifier is updated."""
        for reciever in self._recievers:
            if isinstance(reciever, TelegramReciever):
                logger.debug("Sending image to %s", reciever.chat_id)
                self._bot.send_photo(reciever.chat_id, image)