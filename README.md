# Home Security System

This project is a home security system that uses a Raspberry Pi and a camera, which detects human presence and sends a message with a picture of the intruder. The system checks connected mac addresses, and if a protector (household member) is home, closes the home security system.


### Hardware Requirements
- Raspberry Pi (an embedded computer)
- Camera (can be anything, I use an old webcam)

### Installation

```bash
$ sudo apt install -y python3-picamera2
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python main.py
```

### Advice
You can use service file provided to run the script with systemd. It would make it run on startup, and restart it if it crashes.