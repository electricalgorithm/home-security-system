"""
The strategy which searches for IP addresses.
"""
from core.utils.program_launcher import run_program, PingCommands
from core.strategies.wifi.base_wifi_strategy import BaseWiFiStrategy
from core.utils.datatypes import WiFiStrategyResult


class IpAddressStrategy(BaseWiFiStrategy):
    """
    The strategy which searches for IP addresses.
    """

    def __init__(self):
        super().__init__()
        # Check if the program is installed.
        try:
            run_program(PingCommands.GET_VERSION_INFO)
        except RuntimeError:
            run_program(PingCommands.INSTALL_PROGRAM)

    def check_protectors(self) -> WiFiStrategyResult:
        """This method checks if there are any protectors around."""
        for protector in self.protectors:
            # Send a ping to the protector.
            output = run_program(PingCommands.PING_TO + " " + protector.address)
            # Check if the ping was successful.
            if "Destination Host Unreachable" not in output:
                print("Protector found: " + protector.name)
                return WiFiStrategyResult(protector, True)
        print("Protector not found.")
        return WiFiStrategyResult(None, False)