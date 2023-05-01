import json

from flask import Flask, request

from helper.openai_api import answerMe
from helper.telegram_api import sendMessage

app = Flask(__name__)


@app.route("/")
def home():
    return "OK", 200


@app.route("/telegram", methods=["POST", "GET"])
def telegram():
    data = request.get_json()

    message = data["message"]

    query = message["text"]
    print(query)

    sender_id = message["from"]["id"]

    response = answerMe(query)

    sendMessage(sender_id, response)

    return "OK", 200
