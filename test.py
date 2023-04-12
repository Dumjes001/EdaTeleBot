import requests

import os

from dotenv import load_dotenv

load_dotenv()

bot = os.getenv("TELEGRAM_BOT_TOKEN")
webhook_url = "https://edatelebot.herokuapp.com/telegram-updates"

url = f"https://api.telegram.org/bot{bot}/setWebhook"
data = {"url": webhook_url}

response = requests.post(url, data=data)
print(response.json())
