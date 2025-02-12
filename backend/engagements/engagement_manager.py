import os
from backend.engagements.llm import LLM
from backend.engagements.pages import PageManager, Page
from backend.engagements.engagement_data import EngagementData
from backend.engagements.engagement import Engagement
from backend.engagements.engagement_data_manager import EngagementDataManager


class EngagementManager:
    def __init__(self, llm: LLM, data_path):
        self.file_path = os.path.join(data_path, "engagements.pickle")
        self.llm = llm
        self.data_manager = EngagementDataManager(data_path)

    def get_slugs(self):
        return self.data_manager.get_slugs()

    def wrap_engagement_data(self, data: EngagementData) -> Engagement:
        return Engagement(self.data_manager, self.llm, data)

    def get_engagement(self, slug: str) -> Engagement:
        engagement_data = self.data_manager.get_engagement_data(slug)
        return self.wrap_engagement_data(engagement_data)

    def get_engagements(self):
        engagements = {}
        for slug in self.data_manager.get_slugs():
            engagements[slug] = self.get_engagement(slug)
        return engagements

    def get_page_manager(self) -> PageManager:
        return self.data_manager.get_page_manager()

    def get_page(self, url: str) -> Page:
        return self.get_page_manager().get_page(url)

    def add_engagement(self, engagement: Engagement) -> None:
        self.data_manager.add_engagement_data(engagement.get_data())

    def create_engagement_from_url(self, url):
        engagement = Engagement(self.data_manager, self.llm, self.get_page(url))
        self.add_engagement(engagement)
        return engagement
