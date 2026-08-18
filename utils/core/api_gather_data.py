import requests
from utils.core.states import state
import utils.core.failed_api_request_handler as farh

#Function to get the api data given a url, and if necessary a API Key (and maybe some custom timeout)
def gather_api_data(link,API_KEY=None,timeout=10):

    #Tries to get the data from the api endpoint
    try:
        #Get the endpoint response
        response = requests.get(url=link,headers=API_KEY,timeout=timeout)

        #Checks fof HTTP errors
        response.raise_for_status()

        #Translates the response into a python dictionary
        data = response.json()

        #Checks if the API considered the data gathering succesful 
        if not data.get("success", False):
            cause = data.get("cause", "Unknown reason")
            farh.failed_request(f"[WARNING] Hypixel API rejected the request: {cause}")
            return None

        #Resets the failed api requests counter
        if state.api.failed_requests > 0:
            farh.reset_failed_Request()

        #Set the connection as succesful
        state.api.connection = True

        #Returns the data (kinda obvious)
        return data

    #Handles with errors by doing nothing about it and asking another function on another file to take care of it
    except requests.exceptions.Timeout:
        farh.failed_request("[WARNING] Request timed out.")
        return None

    except requests.exceptions.ConnectionError:
        farh.failed_request("[WARNING] Could not connect to the Hypixel API.")
        return None
    
    except requests.exceptions.HTTPError as e:
        farh.failed_request(f"[WARNING] HTTP {response.status_code} - {e}")
        return None

    except requests.exceptions.RequestException as e:
        farh.failed_request(f"[WARNING] Request failed: {e}")
        return None

    except Exception as e:
        farh.failed_request(f"[WARNING] {e}")
        return None