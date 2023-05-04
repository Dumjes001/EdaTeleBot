import requests

import os

import json

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def sendMessage(sender_id: int, message: str) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {"chat_id": sender_id, "text": str(message)}

    headers = {"Content-Type": "application/json"}

    requests.request("POST", url, data=json.dumps(payload), headers=headers)
