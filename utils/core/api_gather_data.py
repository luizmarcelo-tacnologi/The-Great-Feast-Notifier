import requests

def gather_api_data(link,API_KEY=None,timeout=10):
    
    try:
        response = requests.get(url=link,headers=API_KEY,timeout=timeout)
    
        response.raise_for_status()
    
        data = response.json()
    
        if not data.get("success", False):
            cause = data.get("cause", "Unknown reason")
            return {
                'success': False,
                'cause': f"[WARNING] Hypixel API rejected the request: {cause}",
                'data': None
            }

        return {
            'success': True,
            'cause': None,
            'data': data
        }

    except requests.exceptions.Timeout:
        return {
            'success': False,
            'cause': "[WARNING] Request timed out.",
            'data': None
        }

    except requests.exceptions.ConnectionError:
        return {
            'success': False,
            'cause': "[WARNING] Could not connect to the Hypixel API.",
            'data': None
        }
    
    except requests.exceptions.HTTPError as e:
        return {
            'success': False,
            'cause': f"[WARNING] HTTP {response.status_code} - {e}",
            'data': None
        }

    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'cause': f"[WARNING] Request failed: {e}",
            'data': None
        }

    except Exception as e:
        return {
            'success': False,
            'cause': f"[WARNING] {e}",
            'data': None
        }