import os

import requests

from flask import Flask, request

import telebot

from langchain import OpenAI

from gpt_index import (
    SimpleDirectoryReader,
    GPTSimpleVectorIndex,
    LLMPredictor,
    PromptHelper,
)

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))

aiKey = os.getenv("OPENAI_API_KEY")

index = None


def construct_index(directory_path):
    # set the maximum input size
    max_input_size = 4096

    # set the number of output tokens
    num_outputs = 256

    # set the maximum chunk overlap
    max_chunk_overlap = 20

    # set the chunk size limit
    chunk_size_limit = 600

    # define the Logical learning Machine
    llm_predictor = LLMPredictor(
        llm=OpenAI(
            temperature=0,
            model_name="text-davinci-003",
            max_tokens=num_outputs,
            openai_api_key=aiKey,
            # timeout=60,
        )
    )

    prompt_helper = PromptHelper(
        max_input_size,
        num_outputs,
        max_chunk_overlap,
        chunk_size_limit=chunk_size_limit,
    )

    documents = SimpleDirectoryReader(directory_path).load_data()

    index = GPTSimpleVectorIndex(
        documents,
        llm_predictor=llm_predictor,
        prompt_helper=prompt_helper,
        # verbose=True,
    )

    index.save_to_disk("index.json")


# This function initiates the greeting of a user on addition to the group
@bot.message_handler(func=lambda message: message.new_chat_member)
def greet_new_member(message):
    for new_member in message.new_chat_members:
        bot.send_message(
            chat_id=message.chat.id,
            text=f"{new_member.first_name}, you are welcome to EdaFace Global Community!",
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=f"Hi! Everyone we have a new member joining us, let's give them a warm welcome.",
        )


# This initiates the bot on the activation of the keystroke input ("start" or "help") by the user
@bot.message_handler(commands=["start", "help"])
def start_handler(message):
    bot.send_message(
        chat_id=message.chat.id,
        text="Hello! I'm Eda, your virtual assistant. How may I assist you?",
    )


# This function initiates the response to prompts made by the user
@bot.message_handler(func=lambda message: True)
def message_handler(message):
    query = message.text
    if index is not None:
        response = index.query(query, response_mode="compact", verbose=False)
        # bot.send_message(chat_id=message.chat.id, text=response.response)
    else:
        bot.send_message(
            chat_id=message.chat_id,
            text="Sorry, I'm not available right now. please try again later.",
        )


WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# This function polls the bot on satisfaction of all the neccessary requirements
if __name__ == "__main__":
    if aiKey and WEBHOOK_URL:
        construct_index("C:\\Users\\USER\\Desktop\\SOFTWARE DEVELOPMENT\\EdaBot\\Info")
        index = GPTSimpleVectorIndex.load_from_disk("index.json")

        bot.set_webhook(url=WEBHOOK_URL)

        @app.route("/" + os.getenv("TELEGRAM_BOT_TOKEN"), methods=["POST"])
        def method():
            update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
            bot.process_new_updates([update])
            return "ok"

        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

    else:
        print("OpenAI key not found. Set it in your environment variables.")
