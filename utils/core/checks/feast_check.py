import time
from utils.core.api_gather_data import gather_api_data

SKYBLOCK_EPOCH = 1560275700
SECONDS_PER_SKYBLOCK_DAY = 1200
DAYS_PER_SKYBLOCK_MONTH = 31
DAYS_PER_SKYBLOCK_YEAR = 372

def check_for_feast():

    finnegan_mayor_grandfeast = False
    finnegan_minister_grandfeast = False
    finnegan_running_grandfeast = False
    harvest_feast = False

    api_data = gather_api_data("https://api.hypixel.net/v2/resources/skyblock/election")

    if not api_data.get('success'):
        return{
        'success': False,
        'cause': api_data['cause'],
        'finnegan_mayor_grandfeast': None,
        'finnegan_minister_grandfeast': None,
        'finnegan_running_grandfeast': None,
        'harvest_feast': None
        }

    if api_data['data']['mayor']['name'] == 'Finnegan':
        for mayor_perk in api_data['data']['mayor']['perks']:
            if mayor_perk['name'] == 'Grand Feast':
                finnegan_mayor_grandfeast = True

    if api_data['data']['mayor']['minister']['perk']['name'] == 'Grand Feast':
        finnegan_minister_grandfeast = True

    if 'current' in api_data['data']:
        for candidate in api_data['data']['current']['candidates']:
            if candidate['name'] == 'Finnegan':
                for candidate_perk in candidate['perks']:
                    if candidate_perk['name'] == 'Grand Feast':
                        finnegan_running_grandfeast = True

    now = time.time()
    skyblock_days = (now - SKYBLOCK_EPOCH) // SECONDS_PER_SKYBLOCK_DAY
    day_of_year = skyblock_days % DAYS_PER_SKYBLOCK_YEAR
    month = day_of_year // DAYS_PER_SKYBLOCK_MONTH
    harvest_feast = 6 <= month <= 8

    return{
        'success': True,
        'cause': None,
        'mayor': finnegan_mayor_grandfeast,
        'minister': finnegan_minister_grandfeast,
        'running': finnegan_running_grandfeast,
        'harvest_feast': harvest_feast
    }