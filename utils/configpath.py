import sys
import os

APP_NAME = "TheGreatFeastNotifier"

base_path = None
config_path = None
log_path = None

def get_app_path():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_data_path():
    local_app_data = os.environ.get("LOCALAPPDATA")

    if not local_app_data:
        local_app_data = os.path.expanduser("~")

    path = os.path.join(local_app_data, APP_NAME)
    os.makedirs(path, exist_ok=True)

    return path

def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS,"Atlas", relative_path)
    else:
        return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"Atlas", relative_path)

def set_paths():
    global base_path
    global config_path
    global log_path

    base_path = get_app_path()
    data_path = get_data_path()

    config_path = os.path.join(data_path, "config.json")
    log_path = os.path.join(data_path, "logs.txt")