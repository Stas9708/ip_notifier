import requests


def get_external_ip():
    response = requests.get("https://ipinfo.io")
    data = response.json()
    return data['ip']


