import requests
import time
import json
import threading
import ctypes
import subprocess
import wx
from datetime import datetime
import os

# ultils files
import utils.configpath as cfgp
from utils.logger import log
from utils.notifier import notification
from utils.tray import TrayIcon

APP_ID = "TheGreatFeastNotifier"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)

def load_config():
    global config
    global API_KEY
    global CHECK_INTERVAL
    global set_key_warning

    if not os.path.exists(cfgp.config_path):
        set_key_warning = True
        create_default_config()

    with open(cfgp.config_path, "r") as file:
        config = json.load(file)

    API_KEY = config["api_key"]
    CHECK_INTERVAL = config["check_interval"]

def open_config():
    subprocess.Popen(["notepad.exe", cfgp.config_path])

def open_logs():
    subprocess.Popen(["notepad.exe", cfgp.log_path])

def manual_check():

    global last_mayor_state
    global last_candidate_state
    global last_harvest_feast_state
    global set_key_warning

    last_mayor_state = False
    last_candidate_state = False
    last_harvest_feast_state = False
    set_key_warning = False

    log("[NOTE] Manual Checking!")
    check_once()

def quit_program():
    log("[NOTE] Program Closed")
    stop_event.set()
    wx.CallAfter(wx.GetApp().ExitMainLoop)

def create_default_config():

    default_config = {
        "expiration_date": "",
        "api_key": "",
        "check_interval": 300
    }

    with open(cfgp.config_path, "w", encoding="utf-8") as file:
        json.dump(default_config, file, indent=4)

startup_notification = False
set_key_warning = False
last_elections_cooldown = False
last_mayor_state = False
last_candidate_state = False
last_harvest_feast_state = False
failed_requests = 0
data = None

SKYBLOCK_EPOCH = 1560275700
SECONDS_PER_SKYBLOCK_DAY = 1200
DAYS_PER_YEAR = 372
DAYS_PER_MONTH = 31

cfgp.set_paths()
load_config()
stop_event = threading.Event()
log("[NOTE] Program Started")

def update_status(success):
    current_time = datetime.now().strftime("%H:%M:%S")
    if success:
        status = "Connected"
    else:
        status = "Connection failed"
    tray.menu.update_status(current_time, status)

def failed_request_handler(msg):
    global failed_requests
    failed_requests += 1
    log(msg)
    if failed_requests == 10:
        log("[ERROR] Major Failed Request Streak!")
        notification(
            "Major Failed Request Streak!!!",
            "Check the logs to see what is wrong!",
            "Error.png",
            "minecraft-level-up-sound.wav"
        )

def check_api():

    global data
    global failed_requests
    global set_key_warning
    global startup_notification

    if API_KEY == "":
        if not set_key_warning:
            log("[ERROR] No API Key set!")
            notification(
                "Set your API key on the Settings!",
                "A Hypixel Skyblock API key is required to the program to function! Set one on the Settings!",
                "Error.png",
                "minecraft-level-up-sound.wav"
            )
        set_key_warning = True
        return False
    
    try:
        response = requests.get(
            "https://api.hypixel.net/v2/resources/skyblock/election",
            headers={"API-Key": API_KEY},
            timeout=10
        )
    
        response.raise_for_status()
    
        new_data = response.json()
    
        if not new_data.get("success", False):
            cause = new_data.get("cause", "Unknown reason")
            failed_request_handler(f"[WARNING] Hypixel API rejected the request: {cause}")
            return False

        data = new_data
        
        if failed_requests > 0:
            log(f"[SUCCESS] API request successful after {failed_requests} failed requests")
            if failed_requests >= 10:
                log("[NOTIFICATION] Working fine notification sent!")
                startup_notification = True
                notification(
                    "Everything Working Just Fine!!!",
                    "Don't matter the problem it's all right now!",
                    "banner.png",
                    "minecraft-level-up-sound.wav"
                )
            failed_requests = 0
        return True

    except requests.exceptions.Timeout:
        failed_request_handler("[WARNING] Request timed out.")
        return False

    except requests.exceptions.ConnectionError:
        failed_request_handler("[WARNING] Could not connect to the Hypixel API.")
        return False
    
    except requests.exceptions.HTTPError as e:
        failed_request_handler(f"[WARNING] HTTP {response.status_code} - {e}")
        return False

    except requests.exceptions.RequestException as e:
        failed_request_handler(f"[WARNING] Request failed: {e}")
        return False

    except Exception as e:
        failed_request_handler(f"[WARNING] {e}")
        return False

def check_once():

    load_config()

    global set_key_warning
    global failed_requests
    global startup_notification
    global last_elections_cooldown
    global last_mayor_state
    global last_candidate_state
    global last_harvest_feast_state
    global data

    elections_cooldown = False
    finnegan_mayor_grandfeast = False
    finnegan_running_grandfeast = False
    harvest_feast = False

    success_api_check = check_api()
    wx.CallAfter(update_status, success_api_check)
    if not success_api_check:
        if not startup_notification and failed_requests == 1 and not set_key_warning:
            notification(
                "Not Initialized Correctly!!!",
                "Something isn't working! Check the logs!",
                "Error.png",
                "minecraft-level-up-sound.wav"
            )
        return

    if data['mayor']['name'] == 'Finnegan':
        for mayor_perk in data['mayor']['perks']:
            if mayor_perk['name'] == 'Grand Feast':
                finnegan_mayor_grandfeast = True

    candidates = data.get("current", {}).get("candidates")
    if candidates is None and not last_elections_cooldown:
        elections_cooldown = True
        log("[DATA_WARNING] No data for next election's candidates!")
    else:
        for candidate in data['current']['candidates']:
            if candidate['name'] == 'Finnegan':
                for candidate_perk in candidate['perks']:
                    if candidate_perk['name'] == 'Grand Feast':
                        finnegan_running_grandfeast = True

    now = time.time()
    skyblock_days = (now - SKYBLOCK_EPOCH) // SECONDS_PER_SKYBLOCK_DAY
    day_of_year = skyblock_days % DAYS_PER_YEAR
    month = day_of_year // DAYS_PER_MONTH
    harvest_feast = 6 <= month <= 8

    if finnegan_mayor_grandfeast and not last_mayor_state:
        log("[NOTIFICATION] Finnegan elected with Grand Feast Notification Sent")
        notification(
            "Grand Feast!!!",
            "Finnegan is now the mayor with Grand Feast!",
            "banner.png",
            "minecraft-level-up-sound.wav"
        )

    if finnegan_running_grandfeast and not last_candidate_state:
        log("[NOTIFICATION] Finnegan running with Grand Feast Notification Sent")
        notification(
            "Grand Feast!!! (Probably...)",
            "Finnegan is running with Grand Feast!",
            "banner.png",
            "minecraft-level-up-sound.wav"
        )

    if harvest_feast and not last_harvest_feast_state:
        log("[NOTIFICATION] Harvest Feast detected and Notification sent.")
        notification(
            "Harvest Feast!",
            "It's harvesting season!",
            "banner.png",
            "minecraft-level-up-sound.wav"
        )

    if not (finnegan_mayor_grandfeast or finnegan_running_grandfeast or harvest_feast or startup_notification):
        notification(
            "The searching started!",
            "You will get notitfied when any Feast is detected!",
            "banner.png",
            "minecraft-level-up-sound.wav"
            )
        startup_notification = True

    last_mayor_state = finnegan_mayor_grandfeast
    last_candidate_state = finnegan_running_grandfeast
    last_harvest_feast_state = harvest_feast
    last_elections_cooldown = elections_cooldown
    startup_notification = True

def check_loop():
    while not stop_event.is_set():
        check_once()
        stop_event.wait(CHECK_INTERVAL)

app = wx.App(False)

tray = TrayIcon(check_now=manual_check,open_config=open_config,open_logs=open_logs,quit_program=quit_program)

threading.Thread(target=check_loop,daemon=True).start()

app.MainLoop()

#Build code:
#py -m PyInstaller --onefile --noconsole --icon=Atlas/hypixel.ico --add-data "Atlas;Atlas" TheGreatFeastNotifier.py