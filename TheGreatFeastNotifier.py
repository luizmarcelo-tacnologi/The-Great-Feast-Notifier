import threading
import ctypes
import wx
import json
import datetime

# ultils files
import utils.base.configpath as cfgp
import utils.base.configmng as cfmng
from utils.base.logger import log
from utils.base.notifier import notification
from utils.core.checks.feast_check import check_for_feast
from utils.core.tray import TrayIcon
from utils.core.states import state
from utils.menu.window import SettingsWindow,LogsWindow

#Set the program name
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("TheGreatFeastNotifier")

#Set the paths to the files used
cfgp.set_paths()

#Define the config file and the event to stop the main loop
config = cfmng.load_config()
stop_event = threading.Event()

#Logs that the program started
log("[NOTE] Program Started")

#Defines the buttons used on the menus

def check_now_button():
    state.checks.feast.reset()
    log("[NOTE] Manual Checking!")
    check_once()

def open_config_button():
    settings_window.Show()
    settings_window.Raise()

def open_logs_button():
    logs_window.refresh_logs()
    logs_window.Show()
    logs_window.Raise()

def quit_program_button():
    log("[NOTE] Program Closed")
    stop_event.set()
    wx.CallAfter(wx.GetApp().ExitMainLoop)

def save_settings_button(config):
    with open(cfgp.config_path,"w",encoding="utf-8") as file:
            json.dump(config,file,indent=4)
    cfmng.load_config()

#Updates the menu's Last Checked section
def update_status(success):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    if success:
        status = "Connected"
    else:
        status = "Connection failed"
    tray.menu.update_status(current_time, status)

#The loop that will be in charge of checking the data to send notifications and log about it
def check_once():

    #To use the acess the program states
    global state

    #Get the feast data
    feast_data = check_for_feast()

    #Runs the Last Checked updater
    wx.CallAfter(update_status, feast_data['success'])

    #In case the api check fails
    if not feast_data['success']:
        state.init.startup_notification = True
        state.api.failed_api_requests += 1
        log(feast_data['cause'])
        if state.api.failed_api_requests == 10:
            log("[ERROR] Major Failed Request Streak!")
            notification(
                "Major Failed Request Streak!!!",
                "Check the logs to see what is wrong!",
                "Error.png",
                "minecraft-level-up-sound.wav"
            )
        return

    #To reset the failed_api_requests counter
    if state.api.failed_api_requests > 0:
        log(f"[SUCCESS] API request successful after {state.api.failed_api_requests} failed requests")
        if state.api.failed_api_requests >= 10:
            log("[NOTIFICATION] Working fine notification sent!")
            notification(
                "Everything Working Just Fine!!!",
                "Don't matter the problem it's all right now!",
                "banner.png",
                "minecraft-level-up-sound.wav"
            )
        state.api.failed_api_requests = 0

    #Test to send the notification about finnegan being mayor with the Great Feast perk
    if feast_data['mayor'] and not state.checks.feast.mayor:
        state.init.startup_notification = True
        log("[NOTIFICATION] Finnegan elected with Grand Feast Notification Sent")
        notification(
            "Grand Feast!!!",
            "Finnegan is now the mayor with Grand Feast!",
            "banner.png",
            "minecraft-level-up-sound.wav"
        )

    #Test to send the notification about finnegan being minister with the Great Feast perk
    if feast_data['minister'] and not state.checks.feast.minister:
        state.init.startup_notification = True
        log("[NOTIFICATION] Finnegan elected as a minister with Grand Feast Notification Sent")
        notification(
            "Grand Feast!!!",
            "Finnegan is not the mayor, but minister with Grand Feast!",
            "banner.png",
            "minecraft-level-up-sound.wav"
        )
    
    #Test to send the notification about finnegan being candidate with the Great Feast perk
    if feast_data['running'] and not state.checks.feast.candidate:
        state.init.startup_notification = True
        log("[NOTIFICATION] Finnegan running with Grand Feast Notification Sent")
        notification(
            "Grand Feast!!! (Probably...)",
            "Finnegan is running with Grand Feast!",
            "banner.png",
            "minecraft-level-up-sound.wav"
        )

    #Test to send the notification about finnegan being candidate with the Great Feast perk
    if feast_data['harvest_feast'] and not state.checks.feast.harvest_feast:
        state.init.startup_notification = True
        log("[NOTIFICATION] Harvest Feast detected and Notification sent.")
        notification(
            "Harvest Feast!",
            "It's harvesting season!",
            "banner.png",
            "minecraft-level-up-sound.wav"
        )

    #Test to send the startup notification
    if not (feast_data['mayor'] or feast_data['minister'] or feast_data['running'] or feast_data['harvest_feast'] or state.init.startup_notification):
        notification(
            "The searching started!",
            "You will get notitfied when any Feast is detected!",
            "banner.png",
            "minecraft-level-up-sound.wav"
        )
        state.init.startup_notification = True

    #Set the gathered states
    state.checks.feast.mayor = feast_data['mayor']
    state.checks.feast.minister = feast_data['minister']
    state.checks.feast.candidate = feast_data['running']
    state.checks.feast.harvest_feast = feast_data['harvest_feast']

#The main checking loop that runs on a separate thread
def check_loop():
    while not stop_event.is_set():
        check_once()
        stop_event.wait((cfmng.load_config()['check_interval'])*60)

#Set the GUI app
app = wx.App(False)

#Checks for another instance and close the program if it does find one
instance_checker = wx.SingleInstanceChecker("TheGreatFeastNotifier")
if instance_checker.IsAnotherRunning():
    raise SystemExit

#Defines the auxiliar settings and logs windows
settings_window = SettingsWindow(config,save_settings_button)
logs_window = LogsWindow()

#Defines the program's tray icon
tray = TrayIcon(
    check_now=check_now_button,
    open_config=open_config_button,
    open_logs=open_logs_button,
    quit_program=quit_program_button
)

#Waits for the menus to load before start checking the api
def checking_thread():
    threading.Thread(target=check_loop,daemon=True).start()
wx.CallAfter(checking_thread)

#Runs the GUI app
app.MainLoop()

#Build code:
#py -m PyInstaller --onefile --noconsole --icon=Atlas/hypixel.ico --add-data "Atlas;Atlas" TheGreatFeastNotifier.py