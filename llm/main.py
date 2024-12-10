import os

from dotenv import load_dotenv
from urllib.parse import urlunparse

from llm import LLM


# https://stackoverflow.com/a/15799706
def URL(scheme, netloc, url="", path="", query="", fragment=""):
    return urlunparse((scheme, netloc, url, path, query, fragment))


def get_env():
    load_dotenv()
    ollama_url = URL(
        scheme="http", netloc=f"{os.getenv("OLLAMA_HOST")}:{os.getenv("OLLAMA_PORT")}"
    )
    ollama_model_name = os.getenv("OLLAMA_MODEL")
    return ollama_url, ollama_model_name


if __name__ == "__main__":
    ollama_url, ollama_model_name = get_env()
    llm = LLM(ollama_url, ollama_model_name)
