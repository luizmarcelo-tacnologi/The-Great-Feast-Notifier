import os
import json
import utils.base.configpath as cfgp

#The function to load the config
def load_config():

    #Checks if a config file exisists
    if not os.path.exists(cfgp.config_path):
        create_default_config()

    #Returns the config file open
    with open(cfgp.config_path, "r") as file:
        return json.load(file)

#The funtion to create a default config
def create_default_config():

    #For now it's quite small
    default_config = {
        "check_interval": 5
    }

    #Saves the default config
    with open(cfgp.config_path, "w", encoding="utf-8") as file:
        json.dump(default_config, file, indent=4)