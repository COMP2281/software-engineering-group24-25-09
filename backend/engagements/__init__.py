import os
import pickle
from .engagement import Engagement
from .pages import PageManager


class EngagementManager:
    def file_exists(self):
        return os.path.isfile(self.file_path)

    def load_engagements(self):
        if self.file_exists():
            file = open(self.file_path, "rb")
            self.engagements = pickle.load(file)

    def __init__(self, data_path):
        self.file_path = os.path.join(data_path, "engagements.pickle")
        self.page_manager = PageManager(data_path)
        self.engagements = {}
        self.load_engagements()
