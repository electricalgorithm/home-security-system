from typing import Any
import requests
from requests.auth import HTTPBasicAuth
import os
import glob
import json

def read_latest_file(dir_path: str) -> str:
    """This method reads the latest file from the given directory."""
    # Check if ~ is used.
    if dir_path.startswith("~"):
        dir_path = os.path.expanduser(dir_path)
    
    # Check if the directory exists.
    if not os.path.exists(dir_path):
        raise FileNotFoundError(f"The given directory path does not exist: {dir_path}")
    
    # Get the latest file.
    list_of_files = glob.glob(dir_path + '/*')
    return max(list_of_files, key=os.path.getctime)

def upload_to_fileio(file_path: str) -> str:
    """Uploads a image file to File.io server."""
    with open(".config.json", "r") as file:
        _config = json.load(file)
    file_io_key = _config['file_io_key']

    response = requests.post(
        'https://file.io/',
        files={"file": open(file_path, 'rb')},
        auth=HTTPBasicAuth(file_io_key, '')
    )
    res: dict[str, Any] = response.json()
    if res['success'] == True: 
        return res['link']
    else:
        return "File upload failed!"
