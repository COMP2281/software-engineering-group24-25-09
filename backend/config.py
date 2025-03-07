import os
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


def get_engagement_manager_config() -> bool:
    ignore_robots_file = os.getenv("IGNORE_ROBOTS_FILE")
    return True if ignore_robots_file == "True" else False


load_config()
