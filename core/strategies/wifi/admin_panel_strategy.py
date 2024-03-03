"""
The strategy which searches for MAC addresses using Admin Panel.
"""
from typing import Any

import requests
from bs4 import BeautifulSoup

from core.strategies.wifi.base_wifi_strategy import BaseWiFiStrategy
from core.utils.datatypes import ConnectedDeviceResult, WiFiStrategyResult
from core.utils.logger import get_logger

# Add logging support.
logger = get_logger(__name__)


class AdminPanelStrategy(BaseWiFiStrategy):
    """
    The strategy which searches for MAC addresses using Admin Panel.
    """

    def __init__(self, login_data: dict[str, Any]) -> None:
        """Constructor for AdminPanelStrategy."""
        super().__init__()
        self._login_data: dict[str, Any] = login_data

    def check_protectors(self) -> WiFiStrategyResult:
        """This method checks if there are any protectors around."""
        for protector in self.protectors:
            # Check if the protector is connected to the network.
            if protector.address in [device.address for device in self._get_all_connected()]:
                logger.debug("Protector found: %s", protector.name)
                return WiFiStrategyResult(protector, True)
        logger.debug("No protectors found.")
        return WiFiStrategyResult(None, False)

    # Internal methods
    def _get_all_connected(self) -> list[ConnectedDeviceResult]:
        """This method returns a list of addresses of the clients connected to the network."""
        # Create a session to store cookies.
        session = requests.Session()
        session.get("http://192.168.1.95/login_security.html")
        session.post(
            "http://192.168.1.95/Forms/login_security_1",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": "http://192.168.1.95/login_security.html",
            },
            data=self._login_data
        )

        # Get the response for the page with MAC address list.
        response = session.get("http://192.168.1.95/status/status_deviceinfo.htm")

        # Parse the response.
        soup = BeautifulSoup(response.text, "html.parser")
        tabdata = soup.find_all("td", class_="tabdata")

        # Get the MAC addresses.
        mac_addrs: list[str] = [
            element.text
            for element in tabdata
            if len(element.text) == 17
        ]
        session.close()

        logger.debug("Connected devices: %s", str(mac_addrs))
        return [ConnectedDeviceResult(mac_addr.upper()) for mac_addr in mac_addrs]
