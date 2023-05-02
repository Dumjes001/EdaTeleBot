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

    user_name = message["from"]["username"]

    sender_id = message["from"]["id"]

    words = query.split(" ")

    if words[0] == "/start":
        sendMessage(
            sender_id,
            f"Hi! {user_name}. I am Eddy, the EdaFace Tutor. \n How may i be of assistance?",
        )
    else:
        response = answerMe(query)

        sendMessage(sender_id, response)

    return "OK", 200
