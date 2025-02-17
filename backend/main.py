import os
from backend.data.urls import urls
from backend.engagements.llm import LLM
from engagements import EngagementManager
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
    ollama_model_name = os.getenv("OLLAMA_MODEL")
    return ollama_url, ollama_model_name


if __name__ == "__main__":
    load_config()
    ollama_url, ollama_model_name = get_llm_config()
    llm = LLM(ollama_url, ollama_model_name)
    engagement_manager = EngagementManager(llm, "./data")

    print(engagement_manager.get_engagements())
    for url in urls:
        engagement = engagement_manager.create_engagement_from_url(url)

    slugs = engagement_manager.get_slugs()
    engagement = engagement_manager.get_engagement(slugs[0])
    print(engagement.get_slug())
    print(engagement.get_source_urls())
