import requests
import os


def error_handle():

    url = "https://api.openai.com/v1/engines/davinci-codex/completions"

    response = requests.get(url)

    if response.status_code == 200:
        # The data was successful
        data = response.json
    else:
        print(f"Requests failed with the status code {response.status_code}")

    return "ok"
