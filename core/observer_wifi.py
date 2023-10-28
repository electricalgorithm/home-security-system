"""
This module contains the ObserverWifi class.
"""

import subprocess
from core.internals import Protector


class ObserverWifi:
    """This class is a namespace for all the operations related to network observation."""

    def __init__(self):
        """This method initializes the ObserverWifi class."""
        self._protectors: list[Protector] = []

    def add_protectors(self, protector: Protector):
        """This method adds a protector to the list of protectors."""
        self._protectors.append(protector)

    def remove_protectors(self, protector_name: str):
        """This method removes a protector from the list of protectors."""
        for protector in self._protectors:
            if protector.get_name() == protector_name:
                self._protectors.remove(protector)

    def get_connected_mac_addresses(self) -> list[str]:
        """This method returns a list of MAC addresses of the clients connected to the network."""
        # Run the command to get the list of MAC addresses
        command = "sudo arp-scan --localnet | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'"
        process = subprocess.Popen(command,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE
                                   )
        output, error = process.communicate()

        if error:
            raise RuntimeError(error)

        # Decode the output
        output = output.decode('utf-8')

        # Split the output into a list of MAC addresses
        mac_addrs = output.split('\n')
        mac_addrs = mac_addrs[:-1]

        return mac_addrs

    def check_if_protectors_are_present(self) -> bool:
        """This method checks if there are any protectors around."""
        # Get the list of MAC addresses of the connected clients
        connected_mac_addrs = self.get_connected_mac_addresses()

        # Get the list of MAC addresses of the known clients
        known_mac_addrs = [protector.mac_addr for protector in self._protectors]

        # Check if there are any protectors around.
        for mac_addr in connected_mac_addrs:
            if mac_addr in known_mac_addrs:
                return True
        return False
