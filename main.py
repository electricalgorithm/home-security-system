"""
Main application layer for Home Security System.
"""
from time import sleep
from core.internals import Protector
from core.observer_eye import ObserverEye
from core.observer_wifi import ObserverWifi


def main():
    """
    This method is the entry point of the application.
    """
    # Create the ObserverWifi object.
    observer_wifi = ObserverWifi()
    observer_wifi.add_protectors(Protector('GokhaniPhone', '00:00:00:00:00:00'))

    while True:
        # Check if unknown visitors are present.
        is_protector_home = observer_wifi.check_if_protectors_are_present()

        # If there are unknown visitors, check if there is a person in front of the camera.
        if not is_protector_home:
            observer_eye = ObserverEye()
            any_humans = observer_eye.detect_humans()

            # If there is a person in front of the camera, send a notification.
            if any_humans:
                print('Sending notification...')
        sleep(30)



if __name__ == "__main__":
    main()
