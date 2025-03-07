from backend.config import (
    get_llm_config,
    get_search_config,
    get_engagement_manager_config,
)
from backend.engagements.engagement_manager import (
    EngagementManager,
    CannotCrawlException,
)
from backend.engagements.pages.page import GetPageException
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

    for url in urls:
        print(url, url.can_crawl())

    print(engagement_manager.get_engagements())
    for url in urls:
        try:
            engagement_manager.create_engagement_from_url(url)
        except CannotCrawlException as e:
            print(e)
        except GetPageException as e:
            print(e)

    slugs = engagement_manager.get_slugs()
    print(slugs)
