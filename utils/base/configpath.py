import sys
import os

#The program name
APP_NAME = "TheGreatFeastNotifier"

#The variables for storing the paths
base_path = None
config_path = None
log_path = None

#Function to get the program path
def get_app_path():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS,"Atlas", relative_path)
    else:
        #This .py is kinda nested
        return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),"Atlas", relative_path)

#Function to set the paths
def set_paths():
    global base_path
    global config_path
    global log_path

    #Get the paths
    base_path = get_app_path()
    data_path = get_data_path()

    #Two really useful paths
    config_path = os.path.join(data_path, "config.json")
    log_path = os.path.join(data_path, "logs.txt")