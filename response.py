import requests

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")


def error_handle():
    
    url = f"https://api.openai.com/v1/engines/davinci-codex/completions{API_KEY}"

    response = requests.get(url)

    if response.status_code == 200:
        # The data was successful
        data = response.json
    else:
        print(f"Requests failed with the status code {response.status_code}")

    return "ok"
