import time
from utils.core.api_gather_data import gather_api_data
from utils.core.states import state
from utils.base.notifier import notification
from utils.base.logger import log

#Set the Slyblock time constants
SKYBLOCK_EPOCH = 1560275700
SECONDS_PER_SKYBLOCK_DAY = 1200
DAYS_PER_SKYBLOCK_MONTH = 31
DAYS_PER_SKYBLOCK_YEAR = 372

#Main function to handle feast detection, notification and logging logic
def check_for_feast():

    #Resets local state variables
    finnegan_mayor_grandfeast = False
    finnegan_minister_grandfeast = False
    finnegan_running_grandfeast = False
    harvest_feast = False

    #Get the data from the api
    api_data = gather_api_data("https://api.hypixel.net/v2/resources/skyblock/election")

    #Checks if the the ghater_api_data() was succesful
    if not state.api.connection:
        return

    #Checks if finnegan is mayor with Great Feast perk
    if api_data['mayor']['name'] == 'Finnegan':
        for mayor_perk in api_data['data']['mayor']['perks']:
            if mayor_perk['name'] == 'Grand Feast':
                finnegan_mayor_grandfeast = True

    #Checks if finnegan is minister with Great Feast perk
    if api_data['mayor']['minister']['perk']['name'] == 'Grand Feast':
        finnegan_minister_grandfeast = True

    #Checks if finnegan is candidate with Great Feast perk
    if 'current' in api_data:
        for candidate in api_data['current']['candidates']:
            if candidate['name'] == 'Finnegan':
                for candidate_perk in candidate['perks']:
                    if candidate_perk['name'] == 'Grand Feast':
                        finnegan_running_grandfeast = True

    #Calculates current Skyblock month
    now = time.time()
    skyblock_days = (now - SKYBLOCK_EPOCH) // SECONDS_PER_SKYBLOCK_DAY
    day_of_year = skyblock_days % DAYS_PER_SKYBLOCK_YEAR
    month = day_of_year // DAYS_PER_SKYBLOCK_MONTH

    #Checks for harvest feast (index 0)
    harvest_feast = 6 <= month <= 8

    #Test to send the notification about finnegan being mayor with the Great Feast perk
    if finnegan_mayor_grandfeast and not state.checks.feast.mayor:
        state.init.startup_notification = True
        log("[NOTIFICATION] Finnegan elected with Grand Feast Notification Sent")
        notification(
            "Grand Feast!!!",
            "Finnegan is now the mayor with Grand Feast!",
            "banner.png",
            "minecraft-level-up-sound.wav"
        )
    
    #Test to send the notification about finnegan being minister with the Great Feast perk
    if finnegan_minister_grandfeast and not state.checks.feast.minister:
        state.init.startup_notification = True
        log("[NOTIFICATION] Finnegan elected as a minister with Grand Feast Notification Sent")
        notification(
            "Grand Feast!!!",
            "Finnegan is not the mayor, but minister with Grand Feast!",
            "banner.png",
            "minecraft-level-up-sound.wav"
        )
        
    #Test to send the notification about finnegan being candidate with the Great Feast perk
    if finnegan_running_grandfeast and not state.checks.feast.candidate:
        state.init.startup_notification = True
        log("[NOTIFICATION] Finnegan running with Grand Feast Notification Sent")
        notification(
            "Grand Feast!!! (Probably...)",
            "Finnegan is running with Grand Feast!",
            "banner.png",
            "minecraft-level-up-sound.wav"
        )
    
    #Test to send the notification about finnegan being candidate with the Great Feast perk
    if harvest_feast and not state.checks.feast.harvest_feast:
        state.init.startup_notification = True
        log("[NOTIFICATION] Harvest Feast detected and Notification sent.")
        notification(
            "Harvest Feast!",
            "It's harvesting season!",
            "banner.png",
            "minecraft-level-up-sound.wav"
        )
    
    #Test to send the startup notification (A lot of tests)
    if not (
        finnegan_mayor_grandfeast or 
        finnegan_minister_grandfeast or 
        finnegan_running_grandfeast or 
        harvest_feast or 
        state.init.startup_notification):
        notification(
            "The searching started!",
            "You will get notitfied when any Feast is detected!",
            "banner.png",
            "minecraft-level-up-sound.wav"
        )
        state.init.startup_notification = True
    
    #Set the gathered states
    state.checks.feast.mayor = finnegan_mayor_grandfeast
    state.checks.feast.minister = finnegan_minister_grandfeast
    state.checks.feast.candidate = finnegan_running_grandfeast
    state.checks.feast.harvest_feast = harvest_feast