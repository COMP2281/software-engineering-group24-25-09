import re
from backend.engagements.llm import LLM
from backend.engagements.pages import Page


def title_to_slug(title: str):
    title = title.strip().lower()
    # space with underscores
    title = re.sub(r" +", "_", title)
    # keep only alphanumeric and _ characters
    return re.sub("[^a-z0-9_]", "", title)


class EngagementData:
    def __init__(self, llm: LLM, page: Page):
        self.source_urls = {page.get_url()}
        self.slug = title_to_slug(llm.title(page))

    def get_slug(self):
        return self.slug

    def get_source_urls(self):
        return self.source_urls

    def add_page_url(self, url):
        self.source_urls.add(url)

    def get_page_urls(self):
        return self.source_urls
