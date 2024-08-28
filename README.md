# Home Security System

This project is a home security system that uses a Raspberry Pi and a camera, which detects human presence and sends a message with a picture of the intruder. The system checks connected mac addresses, and if a protector (household member) is home, closes the home security system.


### Hardware Requirements
- Raspberry Pi (an embedded computer)
- Camera (can be anything, I use an old webcam)

### Installation

```bash
$ sudo apt install -y python3-picamera2 libsystemd-dev
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python hss.py
```

Create a `.config.json` file in the root directory with the following content:

```json
{
    "main_settings": {
        "recievers": [
            {
                "name": "[RECEIVER NAME 1]",
                "tel_no": "[RECEIVER TEL NO 1]",
                "callmebot_key": "[CALLMEBOT_KEY 1]"
            }
        ],
        "protectors": [
            {
                "name": "[PROTECTOR NAME 1]",
                "address": "[PROTECTOR MAC/IP ADDR 1]"
            }
        ]
    },
    "strategy_settings": {
        [...IF NEEDED]
    },
    "file_io_key": "[FILE_IO_KEY]"
}
```

### System Design

```mermaid
---
title: Smart Security System UML Diagram
---

classDiagram

    class IDetectorStrategy {
        <<interface>>
        + detect_humans(ndarry) bool
    }

    IDetectorStrategy <|-- EfficientDetStrategy
    IDetectorStrategy <|-- HOGDescriptorStrategy

    class IEyeStrategy {
        <<interface>>
        + set_detector(IDetectorStrategy): void
        + get_detector() IDetectorStrategy
        + get_frame() ndarray
        + check_if_detected() bool
        - detect_humans() DetectorResults
    }

    IEyeStrategy <|-- PiCameraStrategy
    IEyeStrategy <|-- USBCameraStrategy
    IEyeStrategy *-- IDetectorStrategy

    class INotifierStrategy {
        <<interface>>
        - recievers
        + add_receiver(NotifierReciever) void
        + notify_all(String) void
    }

    INotifierStrategy <|-- WhatsAppStrategy
    INotifierStrategy <|-- TelegramStrategy

    class IWifiStrategy {
        <<interface>>
        - protectors
        + add_protector(Protector) void
        + remove_protector(Protector) void
        + check_protectors() WiFiStrategyResult
    }

    IWifiStrategy <|-- AdminPanelStrategy
    IWifiStrategy <|-- IpAddressStrategy
    IWifiStrategy <|-- MacAddressStrategy


    class ISubject {
        <<interface>>
        - observers: List[IObserver]
        - current_state: ObserverStates
        + attach(IObserver) void
        + detach(IObserver) void
        + notify() void
        + get_state() ObserverStates
        + set_state(ObserverStates)
        + get_default_state() ObserverStates
        + run() void
    }

    ISubject <|-- EyeSubject
    ISubject <|-- WifiSubject

    EyeSubject *-- IEyeStrategy
    WifiSubject *-- IWifiStrategy

    class IObserver {
        <<interface>>
        + update(ISubject)
    }

    class HSSObserver {
        + wifi_state: ObserverStates
        + eye_state: ObserverStates
        - notifier: INotifierStrategy
        + update(ISubject) void
        + set_notifier(INotifierStrategy) void
    }

    IObserver <|-- HSSObserver
    HSSObserver *-- INotifierStrategy

    ISubject "1" o--> "1..*" IObserver
```

### Advice
You can use service file provided to run the script with systemd. It would make it run on startup, and restart it if it crashes.
