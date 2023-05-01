import os

import sys

import json

from gpt_index import (
    SimpleDirectoryReader,
    GPTListIndex,
    GPTSimpleVectorIndex,
    LLMPredictor,
    PromptHelper,
)

from langchain import OpenAI

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

path = "C:\\Users\\USER\\Desktop\\SOFTWARE DEVELOPMENT\\EdaTeleBot\\Information"


def construct_index(path):
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

    docs = SimpleDirectoryReader(path).load_data()

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
