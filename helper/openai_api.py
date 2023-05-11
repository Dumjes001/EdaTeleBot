import os
import sys
import urllib.request
from pathlib import Path
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

def construct_index(url):
    # download file from url and save it locally
    filename = "file.txt"
    urllib.request.urlretrieve(url, filename)

    # set path variable to the local file path
    path = str(Path(filename).resolve())

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


url = "https://www.dropbox.com/sh/8pa2z55h3c03n9v/AABR4OUDfZSkeE_Mg3BgBjVIa?dl=1"
vectorIndex = construct_index(url)

def answerMe(prompt: str) -> dict:
    if not os.path.isfile("index.json"):
        vectorIndex()
    else:
        vIndex = GPTSimpleVectorIndex.load_from_disk("index.json")

        response = vIndex.query(prompt, response_mode="compact")

        return response
