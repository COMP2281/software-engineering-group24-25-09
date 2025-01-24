import os
from scraping import PageManager
from data.urls import urls
from dotenv import load_dotenv
from urllib.parse import urlunparse
from llm import LLM


def URL(scheme: str, netloc: str, url="", path="", query="", fragment=""):
    # https://stackoverflow.com/a/15799706
    return str(urlunparse((scheme, netloc, url, path, query, fragment)))


def get_env():
    load_dotenv()
    ollama_url = URL(
        scheme="http", netloc=f"{os.getenv("OLLAMA_HOST")}:{os.getenv("OLLAMA_PORT")}"
    )
    ollama_model_name = os.getenv("OLLAMA_MODEL")
    return ollama_url, ollama_model_name


if __name__ == "__main__":
    page_manager = PageManager("data/pages.pickle")
    # for url in urls:
    #     page_manager.add_page(url)
    print(page_manager.pages)

    ollama_url, ollama_model_name = get_env()
    llm = LLM(ollama_url, ollama_model_name)
    page = page_manager.get_page(
        "https://www.imperial.ac.uk/news/255517/phase-collaboration-sustainable-futures-between-imperial/"
    )
    print(llm.employees(page.get_markdown_content()))
