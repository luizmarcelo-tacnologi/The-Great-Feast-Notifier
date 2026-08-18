import os
import json
import utils.base.configpath as cfgp

def load_config():

    if not os.path.exists(cfgp.config_path):
        create_default_config()

    with open(cfgp.config_path, "r") as file:
        return json.load(file)

def create_default_config():

    default_config = {
        "check_interval": 5
    }

    with open(cfgp.config_path, "w", encoding="utf-8") as file:
        json.dump(default_config, file, indent=4)