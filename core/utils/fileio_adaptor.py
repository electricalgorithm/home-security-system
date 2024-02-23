"""
This module contains the functionality neccessary
to upload intruder's photos to File.io server before
sending it over WhatsApp.
"""
from typing import Any
import os
import glob
import json
from time import sleep

import requests
from requests.auth import HTTPBasicAuth

from core.utils.logger import get_logger

logger = get_logger(__name__)


def read_latest_file(dir_path: str) -> str:
    """This method reads the latest file from the given directory."""
    # Check if ~ is used.
    if dir_path.startswith("~"):
        dir_path = os.path.expanduser(dir_path)

    # Check if the directory exists.
    if not os.path.exists(dir_path):
        raise FileNotFoundError(f"The given directory path does not exist: {dir_path}")

    # Get the latest file.
    while True:
        list_of_files = glob.glob(dir_path + '/*')
        if len(list_of_files) == 0:
            # Wait for save operation to complete.
            sleep(2)
        else:
            break
    return max(list_of_files, key=os.path.getctime)


def upload_to_fileio(file_path: str) -> str:
    """Uploads a image file to File.io server."""
    with open(".config.json", "r", encoding="utf-8") as file:
        _config = json.load(file)
    file_io_key = _config['file_io_key']

    with open(file_path, 'rb') as file:
        response = requests.post(
            'https://file.io/',
            files={"file": file},
            auth=HTTPBasicAuth(file_io_key, '')
        )

    logger.debug("File.io response: %s", str(response.status_code))

    res: dict[str, Any] = response.json()
    if res['success']:
        return res['link']
    return "File upload failed!"
