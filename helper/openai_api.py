import os

import sys

import requests

from gpt_index import (
    SimpleDirectoryReader,
    GPTSimpleVectorIndex,
    GPTListIndex,
    LLMPredictor,
    PromptHelper,
)
from langchain import OpenAI

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Replace the local path with the shared link URL to the data file
path = "https://www.dropbox.com/sh/8pa2z55h3c03n9v/AABR4OUDfZSkeE_Mg3BgBjVIa?dl=1"

def download_file(url, filename):
    # Send an HTTP GET request to the URL to download the file
    response = requests.get(url)
    with open(filename, "wb") as file:
        file.write(response.content)

def construct_index(path):
    # Download the data file to a local directory
    download_file(path, "data_file.txt")

    # This will use the file as the current working directory
    input_dir = os.getcwd()

    # The rest of your existing code here...
    max_input_size = 4096
    tokens = 256
    max_chunk_overlap = 20
    chunk_size_limit = 600

    # define LLM
    llm_predictor = LLMPredictor(
        llm=OpenAI(
            temperature=0.5,
            model_name="text_davinci-003",
            max_tokens=tokens,
            openai_api_key=OPENAI_API_KEY,
        )
    )

    prompt_helper = PromptHelper(
        max_input_size, tokens, max_chunk_overlap, chunk_size_limit=chunk_size_limit
    )

    docs = SimpleDirectoryReader(input_dir).load_data()

    vectorIndex = GPTSimpleVectorIndex(
        documents=docs, llm_predictor=llm_predictor, prompt_helper=prompt_helper
    )

    vectorIndex.save_to_disk("index.json")

    return vectorIndex


vectorIndex = construct_index(path)


def answerMe(prompt: str) -> dict:
    if not os.path.isfile("index.json"):
        vectorIndex()
    else:
        vIndex = GPTSimpleVectorIndex.load_from_disk("index.json")

        response = vIndex.query(prompt, response_mode="compact")

        return response 
