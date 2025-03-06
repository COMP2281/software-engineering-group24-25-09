import os
from backend.engagements.engagement_manager import EngagementManager
from backend.search.prompts import prompts
from backend.search.search import Search
from backend.engagements.llm import LLM
from dotenv import load_dotenv, find_dotenv
from backend.web import build_url


def load_config():
    load_dotenv(find_dotenv())


def get_llm_config() -> tuple[str, str]:
    return (
        build_url(
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
    engagement_manager = EngagementManager(llm, "data")

    api_key, cse_id = get_search_config()
    search = Search(api_key, cse_id, "data")

    urls = search.search_all(prompts[0:1])

    print(urls)

    print(engagement_manager.get_engagements())
    for url in urls:
        engagement = engagement_manager.create_engagement_from_url(str(url))

    slugs = engagement_manager.get_slugs()
    print(slugs)
