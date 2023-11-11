"""
Main application layer for Home Security System.
"""
import logging
from core.observers.subject.eye_subject import EyeSubject
from core.observers.subject.wifi_subject import WiFiSubject
from core.observers.observer.hss_observer import HomeSecuritySystemObserver
from core.strategies.wifi.ipaddress_strategy import IpAddressStrategy
from core.strategies.eye.camera_strategy import CameraStrategy
from core.strategies.notifier.whatsapp_strategy import WhatsappStrategy
from core.utils.datatypes import WhatsappReciever, Protector


# Add logging support.
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] -- [%(levelname)s] -- %(name)s (%(funcName)s): %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='hss.log',
    filemode='a',
)


def main():
    """
    This method is the entry point of the application.
    """
    # Create a Whatsapp notifier.
    whatsapp_notifier = WhatsappStrategy()
    whatsapp_notifier.add_reciever(WhatsappReciever("Gokhan", "+905555555555"))

    # Create a Protector within IpAddressStrategy.
    ip_address_strategy = IpAddressStrategy()
    ip_address_strategy.add_protector(Protector("Gokhan_iPhone", "192.168.X.X"))

    # Create observer.
    hss_observer = HomeSecuritySystemObserver()
    hss_observer.set_notifier(whatsapp_notifier)

    # Create subjects to observe.
    wifi_subject = WiFiSubject()
    wifi_subject.attach(hss_observer)
    eye_subject = EyeSubject("images/")
    eye_subject.attach(hss_observer)

    # Run subjects.
    wifi_subject.run(ip_address_strategy)
    eye_subject.run(CameraStrategy(0))


if __name__ == "__main__":
    main()
