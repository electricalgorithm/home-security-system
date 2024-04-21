"""
This module provides an Telegram bot API to interact with the user
without a direct access to Home Security Service.

Main responsibilities of the servicer as follows:
    - Bot provides if hardware and the bot itself is alive. (/alive)
    - Bot provides if the service is dead or alive. (/health hss.service)
    - Bot restarts the service if the command is sent. (/restart hss.service)
    - Bot provides the latest N logs if wanted. (/logs hss.service:N)
    - Bot provides if protectors are in house, and whose. (/inhouse)
    - Bot provides an image-shot if wanted. (/imageshot)
    - Bot schedules a reboot for the hardware. (/reboot)

"""
import asyncio
import json
from typing import Any

import cv2
from pystemd import systemd1 as systemd
from telebot.async_telebot import AsyncTeleBot

from core.strategies.eye.picamera_strategy import PiCameraStrategy
from core.strategies.wifi.admin_panel_strategy import AdminPanelStrategy


def read_configurations() -> tuple[dict[str, Any], dict[str, Any]]:
    """
    This method reads the configurations from the .config.json file.
    """
    with open(".config.json", "r", encoding="utf-8") as file:
        _config = json.load(file)
    main_settings = _config['main_settings']
    strategy_settings = _config['strategy_settings']
    return main_settings, strategy_settings

# Definitations
MAIN_CONIGS, STRATEGY_CONFIGS = read_configurations()
SERVICER_BOT = AsyncTeleBot(token=STRATEGY_CONFIGS["telegram_strategy"]["bot_key"])
KNOWN_LOG_LOCATIONS: dict[str, str] = {
    "hss.service": "/home/raspberry/.home-security-system/logs/hss.log"
}


@SERVICER_BOT.message_handler(commands=["info", "help", "hi"])
async def info(message):
    """
    This method is called when the /info, /help or /hi command is sent.
    """
    await SERVICER_BOT.reply_to(message, f"Hi, I am the Home Security System Servicer Bot.\n\n"
                                         f"Here are the commands you can use:\n"
                                         f"/alive - provides if hardware and the bot itself is alive.\n"
                                         f"/health hss.service - provides if the service is dead or alive.\n"
                                         f"/restart hss.service - restarts the given service.\n"
                                         f"/logs hss.service:N - provides the latest N logs.\n"
                                         f"/inhouse - provides if protectors are in house, and whose.\n"
                                         f"/imageshot - captures an image and sends.\n"
                                         f"/reboot - reboots the hardware.\n"
                                         f"/info, /help, /hi - this help text.\n")

@SERVICER_BOT.message_handler(commands=['alive'])
async def alive(message):
    """
    This method is called when the /alive command is sent.
    """
    await SERVICER_BOT.reply_to(message, "I am alive.")
    
@SERVICER_BOT.message_handler(commands=['health'])
async def health(message):
    """
    This method is called when the /health command is sent.
    """
    parameters = message.text[len('/health'):]
    service_name = parameters.strip().split(' ')[0]
    with systemd.Unit(service_name.encode("utf-8")) as service:
        active_state: str = service.Unit.ActiveState.decode("utf-8")
        sub_state: str = service.Unit.SubState.decode("utf-8")
        service_name: str = service.Unit.Description.decode("utf-8")
        main_pid: str = service.Service.MainPID
        await SERVICER_BOT.reply_to(message,
                            f"Service: {service_name}\n"
                            f"Active State: {active_state}\n"
                            f"Sub State: {sub_state}\n"
                            f"Main PID: {main_pid}")


@SERVICER_BOT.message_handler(commands=['restart'])
async def restart(message):
    """
    This method is called when the /restart command is sent.
    """
    parameters = message.text[len('/restart'):]
    service_name = parameters.strip().split(' ')[0]
    with systemd.Unit(service_name.encode("utf-8")) as service:
        service.Unit.Restart("fail")
        await SERVICER_BOT.reply_to(message, f"{service_name} is restarted.")


@SERVICER_BOT.message_handler(commands=['logs'])
async def logs(message):
    """
    This method is called when the /logs command is sent.
    """
    first_parameter = message.text[len('/logs'):].strip().split(' ')[0]
    service_name, last_n_lines = first_parameter.split(":")
    if service_name not in KNOWN_LOG_LOCATIONS:
        await SERVICER_BOT.reply_to(message, f"Unknown service: {service_name}")
    with open(KNOWN_LOG_LOCATIONS[service_name], "r") as log_file:
        logs = log_file.readlines()[-int(last_n_lines):]
        await SERVICER_BOT.reply_to(message, "".join(logs))

@SERVICER_BOT.message_handler(commands=['inhouse'])
async def in_house(message):
    """
    This method is called when the /in-house command is sent.
    """
    protectors_list = MAIN_CONIGS["protectors"]
    strategy = AdminPanelStrategy(STRATEGY_CONFIGS["admin_panel_strategy"])
    connected_macs = strategy._get_all_connected()
    connected_protectors = "\n\t- " + "\n\t- ".join([
        protector['name'] for protector in protectors_list
        if protector['address'] in [device.address for device in connected_macs]
    ])
    response = f"Connected MACs: {[device.address for device in connected_macs]}\n\n\n" \
               f"Protectors in house: {connected_protectors}"
    await SERVICER_BOT.reply_to(message, response)
    

@SERVICER_BOT.message_handler(commands=['imageshot'])
async def image_shot(message):
    """
    This method is called when the /image-shot command is sent.
    """
    camera = PiCameraStrategy()
    frame = camera.get_frame()
    success, encoded_frame = cv2.imencode('.png', frame)
    if not success:
        await SERVICER_BOT.reply_to(message, "Failed to capture the image.")
        return
    await SERVICER_BOT.send_photo(message.chat.id, encoded_frame.tobytes())
    del frame, encoded_frame

    
if __name__ == "__main__":
    asyncio.run(SERVICER_BOT.polling())