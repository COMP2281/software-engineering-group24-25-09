import os.path
import pickle


class PageManager:
    def file_exists(self):
        return os.path.isfile(self.file_path)

    def load_pages(self):
        if self.file_exists():
            file = open(self.file_path, "rb")
            self.pages = pickle.load(file)

    def __init__(self, file_path):
        self.file_path = file_path
        self.pages = {}
        self.load_pages()

    def save_pages(self):
        file = open(self.file_path, "wb")
        pickle.dump(self.pages, file)
