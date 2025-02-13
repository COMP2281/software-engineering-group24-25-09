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
    ) -> None:
        """
        Set references to engagement_manager and llm.
        If given a Page then create new EngagementData.
        :param engagement_data_manager: EngagementDataManager instance.
        :param llm: LLM instance.
        :param data: EngagementData or Page to start new EngagementData.
        """
        self.engagement_manager = engagement_data_manager
        self.llm = llm
        if isinstance(data, EngagementData):
            self.data = data
        elif isinstance(data, Page):
            self.data = EngagementData(self.llm, data)

    def get_slug(self) -> str:
        """
        Get the slug identifying the engagement.
        :return: Slug.
        """
        return self.data.get_slug()

    def get_source_urls(self) -> set[str]:
        """
        Get all URLs for the engagement sources.
        :return: Set of source URLs.
        """
        return self.data.get_source_urls()

    def get_data(self) -> EngagementData:
        """
        Get the EngagementData object.
        :return: EngagementData.
        """
        return self.data

    def add_source_url(self, url: str) -> None:
        """
        Add a new source URL to the engagement.
        :param url: Source URL.
        """
        self.data.add_page_url(url)
        self.engagement_manager.save_engagements()
