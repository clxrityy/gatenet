import requests

def get_geo_info(ip: str) -> dict:
    """
    Get geographical information for a given IP address using the ip-api.com service.

    Args:
        ip (str): The IP address to look up.

    Returns:
        dict: A dictionary containing geographical information. Example:
            {
                'status': 'success',
                'country': 'United States',
                'regionName': 'California',
                'city': 'Mountain View',
                ...
            }
        If an error occurs, returns a dict with 'error' and 'message' keys.
    """
    url = f"http://ip-api.com/json/{ip}"
    try:
        response = requests.get(url, timeout=3)
        data = response.json()
        if response.status_code != 200 or data.get('status') == 'fail':
            return {
                'error': True,
                'message': data.get('message', 'Failed to retrieve geo info'),
                'status': data.get('status', 'fail'),
                'query': ip
            }
        return data
    except requests.RequestException as e:
        return {
            'error': True,
            'message': str(e),
            'status': 'fail',
            'query': ip
        }