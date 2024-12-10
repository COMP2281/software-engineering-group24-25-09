import os

from dotenv import load_dotenv
from urllib.parse import urlunparse


# https://stackoverflow.com/a/15799706
def URL(scheme, netloc, url="", path="", query="", fragment=""):
    return urlunparse((scheme, netloc, url, path, query, fragment))


# loading environment variables for API
load_dotenv()
ollama_url = URL(
    scheme="http", netloc=f"{os.getenv("OLLAMA_HOST")}:{os.getenv("OLLAMA_PORT")}"
)
ollama_model_name = os.getenv("OLLAMA_MODEL")

print(ollama_url, ollama_model_name)
