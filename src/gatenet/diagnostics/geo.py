import requests

def get_geo_info(ip: str) -> dict:
    """
    Get geographical information for a given IP address using the ip-api.com service.

    :param ip: The IP address to look up.
    :return: A dictionary containing geographical information or an error message.
    """
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}