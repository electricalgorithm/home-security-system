"""
The strategy which searches for MAC addresses.
"""
from core.utils.program_launcher import run_program, ArpScanCommands
from core.strategies.wifi.base_wifi_strategy import BaseWiFiStrategy
from core.utils.datatypes import WiFiStrategyResult, ConnectedDeviceResult


class MacAddressStrategy(BaseWiFiStrategy):
    """
    The strategy which searches for MAC addresses.
    """
    def __init__(self):
        super().__init__()
        # Check if the program is installed.
        try:
            run_program(ArpScanCommands.GET_VERSION_INFO)
        except RuntimeError:
            run_program(ArpScanCommands.INSTALL_PROGRAM)

    def check_protectors(self) -> WiFiStrategyResult:
        """This method checks if there are any protectors around."""
        for protector in self.protectors:
            if protector.address in [device.address for device in self._get_all_connected()]:
                return WiFiStrategyResult(protector, True)
        return WiFiStrategyResult(None, False)
    
    # Internal methods
    def _get_all_connected(self) -> list[ConnectedDeviceResult]:
        """This method returns a list of addresses of the clients connected to the network."""
        output = run_program(ArpScanCommands.GET_CONNECTED_MAC_ADDRESSES)
        mac_addrs = output.split('\n')
        mac_addrs = mac_addrs[:-1]
        return [ConnectedDeviceResult(mac_addr.upper()) for mac_addr in mac_addrs]
