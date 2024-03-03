"""
This module contains the program launcher functions.
"""
import subprocess
from enum import Enum


class ICommand(Enum, str):
    """Interface for program commands."""


class ArpScanCommands(ICommand):
    """Commands to get connected MAC addresses using ArpScan."""
    GET_VERSION_INFO = "sudo arp-scan --version"
    INSTALL_PROGRAM = "sudo apt-get install arp-scan"
    GET_CONNECTED_MAC_ADDRESSES = "sudo arp-scan --localnet "\
        "| grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'"


class PingCommands(ICommand):
    """Commands to send a ping to a device using ping."""
    GET_VERSION_INFO = "ping --version"
    INSTALL_PROGRAM = "sudo apt-get install iputils-ping"
    PING_TO = "ping -c 1"


def run_program(command: ICommand) -> str:
    """This method runs a program and returns the output and error."""
    output, error = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    ).communicate()
    #  Check if there was an error.
    if error:
        raise RuntimeError(error)

    return output.decode('utf-8')
