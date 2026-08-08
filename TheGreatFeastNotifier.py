import requests
import time
import json
from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading
import ctypes
import subprocess

# ultils files
import utils.configpath as cfgp
from utils.logger import log
from utils.notifier import notification

cfgp.set_paths()

APP_ID = "TheGreatFeastNotifier"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)

def open_config(icon, item):
    subprocess.Popen(["notepad.exe", cfgp.config_path])

def open_logs(icon, item):
    subprocess.Popen(["notepad.exe", cfgp.log_path])

def load_config():
    global config
    global API_KEY
    global CHECK_INTERVAL

    with open(cfgp.config_path, "r") as file:
        config = json.load(file)

    API_KEY = config["api_key"]
    CHECK_INTERVAL = config["check_interval"]

def quit_program(icon, item):
    log("[NOTE] Program Closed")
    stop_event.set()
    icon.stop()

def manual_check(icon, item):
    log("[NOTE] Manual Checking!")
    check_once()

last_mayor_state = False
last_candidate_state = False
last_harvest_feast_state = False
failed_requests = 0
data = None

SKYBLOCK_EPOCH = 1560275700
SECONDS_PER_SKYBLOCK_DAY = 1200
DAYS_PER_MONTH = 31
MONTHS_PER_YEAR = 12

load_config()

stop_event = threading.Event()
image = Image.open(cfgp.resource_path("hypixel.ico"))

menu = Menu(
    MenuItem("Check now", manual_check),
    Menu.SEPARATOR,
    MenuItem("Open config", open_config),
    MenuItem("Open logs", open_logs),
    Menu.SEPARATOR,
    MenuItem("Close", quit_program)
)

icon = Icon(
    "FeastNotifier",
    image,
    "Grand Feast Notifier",
    menu
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
            log(f"[WARNING] Hypixel API rejected the request: {cause}")
            failed_requests += 1
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
        log("[WARNING] Request timed out.")
        failed_requests += 1
        return

    except requests.exceptions.ConnectionError:
        log("[WARNING] Could not connect to the Hypixel API.")
        failed_requests += 1
        return
    
    except requests.exceptions.HTTPError as e:
        log(f"[WARNING] HTTP {response.status_code} - {e}")
        failed_requests += 1
        return

    except requests.exceptions.RequestException as e:
        log(f"[WARNING] Request failed: {e}")
        failed_requests += 1
        return

    except Exception as e:
        log(f"[WARNING] {e}")
        failed_requests += 1
        return

    if failed_requests == 10:
            log("[ERROR] Major Failed Request Streak!")
            notification(
                "Major Failed Request Streak!!!",
                "Check the logs to see what is wrong!",
                "Error.png",
                "minecraft-level-up-sound"
            )
    print(data)

def check_once():
    load_config()
    global last_mayor_state
    global last_candidate_state
    global last_harvest_feast_state
    global failed_requests
    global data

    finnegan_mayor_grandfeast = False
    finnegan_running_grandfeast = False

    check_api()

    if data['mayor']['name'] == 'Finnegan':
        for mayor_perk in data['mayor']['perks']:
            if mayor_perk['name'] == 'Grand Feast':
                finnegan_mayor_grandfeast = True

    for candidate in data['current']['candidates']:
        if candidate['name'] == 'Finnegan':
            for candidate_perk in candidate['perks']:
                if candidate_perk['name'] == 'Grand Feast':
                    finnegan_running_grandfeast = True

    now = time.time()
    skyblock_days = int((now - SKYBLOCK_EPOCH) // SECONDS_PER_SKYBLOCK_DAY)
    day_of_year = skyblock_days % (DAYS_PER_MONTH * MONTHS_PER_YEAR)
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

threading.Thread(target=check_loop,daemon=True).start()

icon.run()

#Build code:
#python -m PyInstaller --onefile --noconsole --icon=Atlas/hypixel.ico --add-data "Atlas;Atlas" TheGreatFeastNotifier.py