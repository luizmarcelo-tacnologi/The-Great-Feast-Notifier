import sys
import os

base_path = None
config_path = None
log_path = None

def set_paths():
    global base_path, config_path, log_path
    if getattr(sys, "frozen", False):
        # Running from the .exe
        base_path = os.path.dirname(sys.executable)
    else:
        # Running from the .py file
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    config_path = os.path.join(base_path, "config.json")
    log_path = os.path.join(base_path, "logs.txt")

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "Atlas", relative_path)
    return os.path.join(base_path, "Atlas", relative_path)