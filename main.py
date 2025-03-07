from backend.config import (
    get_llm_config,
    get_search_config,
    get_engagement_manager_config,
)
from backend.search.prompts import prompts
from backend.search.search import Search
from backend.engagements.llm import LLM


if __name__ == "__main__":
    ollama_url, ollama_model_name = get_llm_config()
    llm = LLM(ollama_url, ollama_model_name)
    ignore_robots_file = get_engagement_manager_config()
    engagement_manager = EngagementManager(llm, "data", ignore_robots_file)

    api_key, cse_id = get_search_config()
    search = Search(api_key, cse_id, "data")

    urls = search.search_all(prompts[0:1])

    print(urls)

    print(engagement_manager.get_engagements())
    for url in urls:
        engagement = engagement_manager.create_engagement_from_url(str(url))

    slugs = engagement_manager.get_slugs()
    print(slugs)
