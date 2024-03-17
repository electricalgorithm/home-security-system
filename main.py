"""
Main application layer for Home Security System.
"""
import json
import sys
from concurrent.futures import wait
from typing import Any

from core.observers.observer.hss_observer import HomeSecuritySystemObserver
from core.observers.subject.eye_subject import EyeSubject
from core.observers.subject.wifi_subject import WiFiSubject
from core.strategies.detectors.efficientdet_strategy import EfficientdetStrategy
from core.strategies.eye.picamera_strategy import PiCameraStrategy
from core.strategies.notifier.whatsapp_strategy import WhatsappStrategy
from core.strategies.wifi.admin_panel_strategy import AdminPanelStrategy
from core.utils.datatypes import Protector, WhatsappReciever


def read_configurations() -> dict[str, Any]:
    """
    This method reads the configurations from the .config.json file.
    """
    with open(".config.json", "r", encoding="utf-8") as file:
        _config = json.load(file)
    main_settings = _config['main_settings']
    strategy_settings = _config['strategy_settings']

    return main_settings, strategy_settings


def main():
    """
    This method is the entry point of the application.
    """
    # Read configurations.
    config, strategy_config = read_configurations()
    # Create a WhatsApp notifier.
    whatsapp_notifier = WhatsappStrategy()
    for reciever in config['recievers']:
        whatsapp_notifier.add_reciever(WhatsappReciever(reciever['name'],
                                                        reciever['tel_no'],
                                                        reciever['callmebot_key']))

    # Create a Protector within IpAddressStrategy.
    ip_address_strategy = AdminPanelStrategy(strategy_config)
    for protector in config['protectors']:
        ip_address_strategy.add_protector(Protector(protector['name'],
                                                    protector['address']))

    # Create observer.
    hss_observer = HomeSecuritySystemObserver()
    hss_observer.set_notifier(whatsapp_notifier)

    #  Create subjects to observe.
    wifi_subject = WiFiSubject()
    wifi_subject.attach(hss_observer)
    eye_subject = EyeSubject()
    eye_subject.attach(hss_observer)

    # Run subjects.
    wifi_subject.run(ip_address_strategy)

    # Set-up the camera to detect humans.
    camera = PiCameraStrategy()
    camera.set_detector(EfficientdetStrategy())
    eye_subject.run(camera, wifi_subject.get_protector_lock())
    
    # Notify that the system is running.
    whatsapp_notifier.notify_all("Home Security System is started.")
    
    # Wait for the futures.
    _, failures = wait([wifi_subject.thread, eye_subject.thread])
    for failure in failures:
        whatsapp_notifier.notify_all("Home Security System has failed to run. Please check the logs.")
        whatsapp_notifier.notify_all("Error: " + str(failure.exception()))
        whatsapp_notifier.notify_all("Result: " + str(failure.result()))
        # Close the application to let systemd re-start it.
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)
