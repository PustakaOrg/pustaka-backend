import requests
from core.settings import WAHA_BASE_URL


def check_status():
    response = requests.get(url=f"{WAHA_BASE_URL}/api/sessions/default")
    if response.status_code == 200:
        status = response.json().get("status")  # STOPPED,STARTING, SCAN_QR, WORKING
        if status == "FAILED" or status == "STOPPED":
            requests.post(f"{WAHA_BASE_URL}/api/sessions/default/restart")
        return status
    return "CONNECTION_ERROR"


def disconnect():
    requests.post(url=f"{WAHA_BASE_URL}/api/sessions/default/logout")


def get_qr_code():
    response = requests.get(url=f"{WAHA_BASE_URL}/api/default/auth/qr?format=raw")
    raw_qr = response.json().get("value")
    return raw_qr

def get_profile():
    response = requests.get(url=f"{WAHA_BASE_URL}/api/default/profile")
    profile = response.json()
    return profile

def send_wa(recepiant, message):
    url = f"{WAHA_BASE_URL}/api/sendText"
    data = {
        "session": "default",
        "chatId": f"{recepiant}@c.us",
        "text": message,
    }
    requests.post(url, json=data)
