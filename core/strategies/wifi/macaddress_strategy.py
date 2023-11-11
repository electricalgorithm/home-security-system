"""
The strategy which searches for MAC addresses.
"""
import logging

from core.utils.program_launcher import run_program, ArpScanCommands
from core.strategies.wifi.base_wifi_strategy import BaseWiFiStrategy
from core.utils.datatypes import WiFiStrategyResult, ConnectedDeviceResult

# Add logging support.
logger = logging.getLogger(__name__)


class MacAddressStrategy(BaseWiFiStrategy):
    """
    The strategy which searches for MAC addresses.
    """
    def __init__(self):
        super().__init__()
        # Check if the program is installed.
        try:
            logger.debug("Checking if the program is installed...")
            run_program(ArpScanCommands.GET_VERSION_INFO)
        except RuntimeError:
            logger.debug("Program is not installed. Installing...")
            run_program(ArpScanCommands.INSTALL_PROGRAM)

    def check_protectors(self) -> WiFiStrategyResult:
        """This method checks if there are any protectors around."""
        for protector in self.protectors:
            # Check if the protector is connected to the network.
            if protector.address in [device.address for device in self._get_all_connected()]:
                logger.debug("Protector found: " + protector.name)
                return WiFiStrategyResult(protector, True)
        logger.debug("No protectors found.")
        return WiFiStrategyResult(None, False)
    
    # Internal methods
    def _get_all_connected(self) -> list[ConnectedDeviceResult]:
        """This method returns a list of addresses of the clients connected to the network."""
        output = run_program(ArpScanCommands.GET_CONNECTED_MAC_ADDRESSES)
        mac_addrs = output.split('\n')
        mac_addrs = mac_addrs[:-1]
        logger.debug("Connected devices: " + str(mac_addrs))
        return [ConnectedDeviceResult(mac_addr.upper()) for mac_addr in mac_addrs]
