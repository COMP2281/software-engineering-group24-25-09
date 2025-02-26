import os
from backend.engagements.engagement_manager import EngagementManager
from data.urls import urls
from backend.engagements.llm import LLM
from backend.search import Search, prompts
from dotenv import load_dotenv, find_dotenv
from urllib.parse import urlunparse


def URL(scheme: str, netloc: str, url="", path="", query="", fragment=""):
    # https://stackoverflow.com/a/15799706
    return str(urlunparse((scheme, netloc, url, path, query, fragment)))


def load_config():
    load_dotenv(find_dotenv())


def get_llm_config() -> tuple[str, str]:
    return (
        URL(
            scheme="http",
            netloc=f"{os.getenv("OLLAMA_HOST")}:{os.getenv("OLLAMA_PORT")}",
        ),
        os.getenv("OLLAMA_MODEL"),
    )


def get_search_config() -> tuple[str, str]:
    return os.getenv("GOOGLE_API_KEY"), os.getenv("GOOGLE_CSE_ID")


if __name__ == "__main__":
    load_config()
    ollama_url, ollama_model_name = get_llm_config()
    llm = LLM(ollama_url, ollama_model_name)
    engagement_manager = EngagementManager(llm, "./data")

    api_key, cse_id = get_search_config()
    search = Search(api_key, cse_id, "backend/data")

    urls = search.search_all(prompts[0:1])

    print(urls)

    print(engagement_manager.get_engagements())
    for url in urls:
        engagement = engagement_manager.create_engagement_from_url(str(url))

    slugs = engagement_manager.get_slugs()
