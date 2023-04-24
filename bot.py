import os

import sys

import time

from dotenv import load_dotenv

from gpt_index import (
    SimpleDirectoryReader,
    GPTListIndex,
    GPTSimpleVectorIndex,
    LLMPredictor,
    PromptHelper,
)

from langchain import OpenAI

import telebot
from telebot import types

load_dotenv()

# Load OpenAI API key from environment variables
openai_api_key = os.getenv("OPEN_AI_KEY")

# Load the directory path
directory_path = (
    "C:\\Users\\USER\\Desktop\\SOFTWARE DEVELOPMENT\\EdaTeleBot\\Information"
)

# Initialize the bot
bot = telebot.TeleBot("TELEGRAM_BOT_TOKEN")


# Construct the Index
def construct_index(path):
    max_input_size = 4096

    tokens = 256

    max_chunk_overlap = 20

    chunk_size_limit = 600

    # define the LLM
    llm_predictor = LLMPredictor(
        llm=OpenAI(
            temperature=0.5,
            model_name="text-davinci-003",
            max_tokens=tokens,
            openai_api_key=openai_api_key,
        )
    )

    prompt_helper = PromptHelper(
        max_input_size, tokens, max_chunk_overlap, chunk_size_limit=chunk_size_limit
    )

    docs = SimpleDirectoryReader(path).load_data()

    vectorIndex = GPTSimpleVectorIndex(
        documents=docs, llm_predictor=llm_predictor, prompt_helper=prompt_helper
    )

    vectorIndex.save_to_disk("index.json")

    return vectorIndex


vectorIndex = construct_index(directory_path)


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
        text="Hello! I'm Eda, your Virtual Assistant. How may I assist you?",
    )


# This function initiates the response to prompts made by the user
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    vIndex = GPTSimpleVectorIndex.load_from_disk(vectorIndex)

    prompt = message.text

    # Query the GPT index
    response = vIndex.query(prompt, response_mode="text")

    # Send response back to the user
    bot.send_message(message.chat.id, response)


# Start the Bot
while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(10)
