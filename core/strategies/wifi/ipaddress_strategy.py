"""
The strategy which searches for IP addresses.
"""
import logging
from core.utils.program_launcher import run_program, PingCommands
from core.strategies.wifi.base_wifi_strategy import BaseWiFiStrategy
from core.utils.datatypes import WiFiStrategyResult

# Add logging support.
logger = logging.getLogger(__name__)


class IpAddressStrategy(BaseWiFiStrategy):
    """
    The strategy which searches for IP addresses.
    """

    def __init__(self):
        super().__init__()
        # Check if the program is installed.
        try:
            run_program(PingCommands.GET_VERSION_INFO)
            logger.debug("Program is already installed.")
        except RuntimeError:
            logger.debug("Program is not installed. Installing...")
            run_program(PingCommands.INSTALL_PROGRAM)

    def check_protectors(self) -> WiFiStrategyResult:
        """This method checks if there are any protectors around."""
        for protector in self.protectors:
            # Send a ping to the protector.
            logger.debug("Sending ping to " + protector.name)
            output = run_program(PingCommands.PING_TO + " " + protector.address)
            # Check if the ping was successful.
            if "Destination Host Unreachable" not in output:
                logger.debug("Protector found: " + protector.name)
                return WiFiStrategyResult(protector, True)
        logger.debug("No protectors found.")
        return WiFiStrategyResult(None, False)