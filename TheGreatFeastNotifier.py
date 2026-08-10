import requests
import time
import json
import threading
import ctypes
import subprocess
import wx

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

    with open(cfgp.config_path, "r") as file:
        config = json.load(file)

    API_KEY = config["api_key"]
    CHECK_INTERVAL = config["check_interval"]

def open_config():
    subprocess.Popen(["notepad.exe", cfgp.config_path])

def open_logs():
    subprocess.Popen(["notepad.exe", cfgp.log_path])

def manual_check():
    log("[NOTE] Manual Checking!")
    check_once()

def quit_program():
    log("[NOTE] Program Closed")
    stop_event.set()
    wx.CallAfter(wx.GetApp().ExitMainLoop)

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
            "minecraft-level-up-sound"
        )

def check_api():

    global data
    global failed_requests

    log("[NOTE] Checking Hypixel API...")
    
    try:
        response = requests.get(
            "https://api.hypixel.net/v2/resources/skyblock/election",
            headers={"API-Key": API_KEY},
            timeout=10
        )
    
        response.raise_for_status()
    
        data = response.json()
    
        if not data.get("success", False):
            cause = data.get("cause", "Unknown reason")
            failed_request_handler(f"[WARNING] Hypixel API rejected the request: {cause}")
            return
        else:
            if failed_requests > 0:
                log(f"[SUCCESS] API request successful after {failed_requests} failed requests")
                failed_requests = 0
                notification(
                    "Everything Working Just Fine!!!",
                    "Don't matter the problem it's all right now!",
                    "banner.png",
                    "minecraft-level-up-sound.wav"
                )
            else:
                log("[NOTE] API request successful.")
                failed_requests = 0

    except requests.exceptions.Timeout:
        failed_request_handler("[WARNING] Request timed out.")
        return

    except requests.exceptions.ConnectionError:
        failed_request_handler("[WARNING] Could not connect to the Hypixel API.")
        return
    
    except requests.exceptions.HTTPError as e:
        failed_request_handler(f"[WARNING] HTTP {response.status_code} - {e}")
        return

    except requests.exceptions.RequestException as e:
        failed_request_handler(f"[WARNING] Request failed: {e}")
        return

    except Exception as e:
        failed_request_handler(f"[WARNING] {e}")
        return
            
    print(data)

def check_once():
    load_config()
    global last_mayor_state
    global last_candidate_state
    global last_harvest_feast_state
    global data

    finnegan_mayor_grandfeast = False
    finnegan_running_grandfeast = False

    check_api()

    if data['mayor']['name'] == 'Finnegan':
        for mayor_perk in data['mayor']['perks']:
            if mayor_perk['name'] == 'Grand Feast':
                finnegan_mayor_grandfeast = True

    try:

        for candidate in data['current']['candidates']:
            if candidate['name'] == 'Finnegan':
                for candidate_perk in candidate['perks']:
                    if candidate_perk['name'] == 'Grand Feast':
                        finnegan_running_grandfeast = True
    except:
        log("[DATA_WARNING] No data for next election's candidates!")

    now = time.time()
    skyblock_days = (now - SKYBLOCK_EPOCH) // SECONDS_PER_SKYBLOCK_DAY
    day_of_year = skyblock_days % DAYS_PER_YEAR
    month = day_of_year // DAYS_PER_MONTH
    harvest_feast = 6 <= month <= 8

    if finnegan_mayor_grandfeast and not last_mayor_state:
        log("[DATA_SUCCESS] Finnegan elected with Grand Feast Notification Sent")
        notification(
            "Grand Feast!!!",
            "Finnegan is now the mayor with Grand Feast!",
            "banner.png",
            "minecraft-level-up-sound"
        )

    if finnegan_running_grandfeast and not last_candidate_state:
        log("[DATA_SUCCESS] Finnegan running with Grand Feast Notification Sent")
        notification(
            "Grand Feast!!! (Probably...)",
            "Finnegan is running with Grand Feast!",
            "banner.png",
            "minecraft-level-up-sound"
        )

    if harvest_feast and not last_harvest_feast_state:
        log("[DATA_SUCCESS] Harvest Feast detected and Notification sent.")
        notification(
            "Harvest Feast!",
            "It's harvesting season!",
            "banner.png",
            "minecraft-level-up-sound"
        )

    last_mayor_state = finnegan_mayor_grandfeast
    last_candidate_state = finnegan_running_grandfeast
    last_harvest_feast_state = harvest_feast

def check_loop():
    global running
    global last_mayor_state
    global last_candidate_state
    global last_harvest_feast_state
    while not stop_event.is_set():

        check_once()
        
        stop_event.wait(CHECK_INTERVAL)

app = wx.App(False)

tray = TrayIcon(check_now=manual_check,open_config=open_config,open_logs=open_logs,quit_program=quit_program)

threading.Thread(target=check_loop,daemon=True).start()

app.MainLoop()

#Build code:
#py -m PyInstaller --onefile --noconsole --icon=Atlas/hypixel.ico --add-data "Atlas;Atlas" TheGreatFeastNotifier.py