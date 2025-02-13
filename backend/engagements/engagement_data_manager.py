import os
import pickle
from backend.engagements.pages import PageManager
from backend.engagements.engagement_data import EngagementData


class EngagementDataManager:
    def file_exists(self) -> bool:
        """
        Check if data file exists.
        :return: True if file exists, False otherwise.
        """
        return os.path.isfile(self.file_path)

    def load_engagements(self) -> None:
        """
        Load engagements from the file if it exists.
        """
        if self.file_exists():
            file = open(self.file_path, "rb")
            self.data = pickle.load(file)

    def __init__(self, data_path: str) -> None:
        """
        Instantiate PageManager and load engagements.
        :param data_path: Path to data directory.
        """
        self.file_path = os.path.join(data_path, "engagements.pickle")
        self.page_manager = PageManager(data_path)
        self.data = {}
        self.load_engagements()

    def save_engagements(self) -> None:
        """
        Save engagements to the file.
        A new file is created if none exists.
        """
        file = open(self.file_path, "wb")
        pickle.dump(self.data, file)

    def get_slugs(self) -> list[str]:
        """
        Get slugs for all engagements.
        :return: List of slugs.
        """
        return list(self.data.keys())

    def get_engagement_data(self, slug: str) -> EngagementData:
        """
        Get the data from the engagement identified by the slug.
        :param slug: Slug identifying the engagement.
        :return: EngagementData for the engagement.
        """
        return self.data[slug]

    def get_page_manager(self) -> PageManager:
        """
        Get the PageManager instance.
        :return: PageManager instance.
        """
        return self.page_manager

    def add_engagement_data(self, engagement_data: EngagementData) -> None:
        """
        Add engagement data to the manager and save it to the file.
        :param engagement_data: EngagementData.
        """
        self.data[engagement_data.get_slug()] = engagement_data
        self.save_engagements()
