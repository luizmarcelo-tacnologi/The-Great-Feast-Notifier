import sys
import os

#The program's name
APP_NAME = "TheGreatFeastNotifier"

#The variables for storing the paths
config_path = None
log_path = None

#Funtion to get the localappdata path
def get_data_path():

    #Gets the localappdata path
    local_app_data = os.environ.get("LOCALAPPDATA")

    #If there isn't one creates one
    if not local_app_data:
        local_app_data = os.path.expanduser("~")

    #Returns the program's folder
    path = os.path.join(local_app_data, APP_NAME)
    os.makedirs(path, exist_ok=True)
    return path

#Function to get the resources path
def resource_path(relative_path):
    #On the .exe form
    if getattr(sys, "frozen", False):
        return os.path.join(os.path.dirname(sys.executable),"_internal","Atlas", relative_path)
    #On the python form
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),"Atlas", relative_path)

#Function to set the paths
def set_paths():
    global config_path
    global log_path

    #Two really useful paths
    config_path = os.path.join(get_data_path(), "config.json")
    log_path = os.path.join(get_data_path(), "logs.txt")