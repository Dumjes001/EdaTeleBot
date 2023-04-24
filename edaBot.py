import os
import sys
import telebot
import time

from logs import (
    get_maxi_logs,
    get_mini_logs,
)

from langchain import OpenAI

from gpt_index import (
    SimpleDirectoryReader,
    GPTSimpleVectorIndex,
    LLMPredictor,
    GPTListIndex,
    PromptHelper,
    readers,
)

from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# Setup Telegram Bot Class
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))

# Setup the OpenAi Object
aiKey = os.getenv("OPENAI_API_KEY")


# Set the directory path for GPT index
directory_path = (
    "C:\\Users\\USER\\Desktop\\SOFTWARE DEVELOPMENT\\EdaTeleBot\\Information"
)

index = None


def construct_index(directory_path):
    # set the maximum input size
    max_input_size = 4096

    # set the number of output tokens
    num_outputs = 256

    # set the maximum chunk overlap
    max_chunk_overlap = 20

    # set the chunk size limit
    chunk_size_limit = 512

    # define the Logical learning Machine
    llm_predictor = LLMPredictor(
        llm=OpenAI(
            temperature=0.5,
            model_name="text-davinci-003",
            max_tokens=num_outputs,
        )
    )
    print(llm_predictor)

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

    print("Index Created Successfully")

    return index


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


def respond(query, bot, chat_id):
    prompt_indices = index.search(query)
    response = index.generate_text_from_indices(prompt_indices)
    bot.send_message(chat_id, response)


# This function initiates the response to prompts made by the user
@bot.message_handler(func=lambda message: True)
def message_handle(message):
    global index

    index = GPTSimpleVectorIndex.load_from_disk("index.json")
    print(index)

    # Handling Incoming query from Telegram Users
    message_text = message.text
    print(message_text)

    chat_id = message.chat.id

    if index is None:
        response = "Index is not available, Please Try Again!"

    else:
        query = message_text
        response = index.generate_output()

    # Call the respond function here
    respond(query, bot, chat_id)


if aiKey:
    if not os.path.isfile("index.json"):
        # Consstruct the GPT Index if it hasn't been created yet
        print("Creating GPT Index")
        index = construct_index(directory_path)
        print("Index Created Successfully!")
    else:
        # Load the existing index if it has already been created
        index = GPTSimpleVectorIndex.load_from_disk("index.json")
        print("Index Loaded Successfully!")

else:
    print("OpenAI Key not found. Please set environment variable.")


while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(10)
