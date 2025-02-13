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
        Load engagements from file if it exists.
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

    def save_engagements(self):
        file = open(self.file_path, "wb")
        pickle.dump(self.data, file)

    def get_slugs(self):
        return list(self.data.keys())

    def get_engagement_data(self, slug):
        return self.data[slug]

    def get_page_manager(self) -> PageManager:
        return self.page_manager

    def add_engagement_data(self, engagement_data: EngagementData) -> None:
        self.data[engagement_data.get_slug()] = engagement_data
        self.save_engagements()
