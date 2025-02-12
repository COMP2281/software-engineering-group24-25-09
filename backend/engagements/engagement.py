from backend.engagements.llm import LLM
from backend.engagements.pages import Page
from backend.engagements.engagement_data import EngagementData
from backend.engagements.engagement_data_manager import EngagementDataManager


class Engagement:
    def __init__(
        self,
        engagement_data_manager: EngagementDataManager,
        llm: LLM,
        data: EngagementData | Page,
    ):
        self.engagement_manager = engagement_data_manager
        self.llm = llm
        if isinstance(data, EngagementData):
            self.data = data
        elif isinstance(data, Page):
            self.data = EngagementData(self.llm, data)

    def get_slug(self):
        return self.data.get_slug()

    def get_source_urls(self):
        return self.data.get_source_urls()

    def get_data(self):
        return self.data

    def add_page_url(self, url: str):
        self.data.add_page_url(url)
        self.engagement_manager.save_engagements()
