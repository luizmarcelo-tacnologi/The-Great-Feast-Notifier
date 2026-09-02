import threading
import ctypes
import wx
import json
import datetime
import time

# ultils files
import utils.base.configpath as cfgp
import utils.base.configmng as cfmng
from utils.base.logger import log,init_logger
from utils.base.notifier import register_app_identity
from utils.core.checks.feast_check import check_for_feast
from utils.base.startup.sessioncheck import SessionMonitor, is_session_locked
from utils.core.tray import TrayIcon
from utils.menu.window import SettingsWindow,LogsWindow
from utils.core.states import state

#Set the program name
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("TheGreatFeastNotifier")

#Set the paths to the files used
cfgp.set_paths()
#Set the app indentity for the notifications
register_app_identity()
#Set the logger
init_logger()

#Define the config file and the events related to the main loop
config = cfmng.load_config()
stop_event = threading.Event()
reescan_event = threading.Event()
login_ready_event = threading.Event()

#Logs that the program started
log("[INFO] Program Started")

#Defines the buttons used on the menus

def check_now_button():
    state.checks.feast.reset()
    log("[INFO] Manual Checking!")
    reescan_event.set()

def open_config_button():
    settings_window.Show()
    settings_window.Raise()

def open_logs_button():
    logs_window.refresh_logs()
    logs_window.Show()
    logs_window.Raise()

def quit_program_button():
    log("[INFO] Program Closed")
    session_monitor.close()
    reescan_event.set()
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

#The main checking loop that runs on a separate thread
def check_loop():

    login_ready_event.wait()
    time.sleep(8)

    while not stop_event.is_set():

        #Get the feast data
        check_for_feast()

        #Runs the Last Checked updater
        wx.CallAfter(update_status, state.api.connection)

        #The event that handles the loop waiting
        reescan_event.wait((config['check_interval'])*60)
        reescan_event.clear()

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

session_monitor = SessionMonitor(login_ready_event.set())
if not is_session_locked():
    login_ready_event.set()

#Waits for the menus to load before start checking the api
def checking_thread():
    threading.Thread(target=check_loop,daemon=True).start()
wx.CallAfter(checking_thread)

#Runs the GUI app
app.MainLoop()

#Build code:
#py -m PyInstaller --onefile --noconsole --icon=Atlas/hypixel.ico --add-data "Atlas;Atlas" TheGreatFeastNotifier.py