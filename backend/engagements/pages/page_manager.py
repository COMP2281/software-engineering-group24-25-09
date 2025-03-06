import os.path
import pickle
from backend.engagements.pages.page import Page


class PageManager:
    def file_exists(self) -> bool:
        return os.path.isfile(self.file_path)

    def load_pages(self) -> None:
        if self.file_exists():
            file = open(self.file_path, "rb")
            self.pages = pickle.load(file)

    def __init__(self, data_path: str) -> None:
        self.file_path = os.path.join(data_path, "pages.pickle")
        self.pages = {}
        self.load_pages()

    def save_pages(self) -> None:
        file = open(self.file_path, "wb")
        pickle.dump(self.pages, file)

    def add_page(self, url: str) -> None:
        if url in self.pages:
            return
        self.pages[url] = Page(url)
        self.save_pages()

    def remove_page(self, url: str) -> None:
        del self.pages[url]
        self.save_pages()

    def update_page(self, url: str) -> None:
        if url not in self.pages:
            return
        self.pages[url].update()
        self.save_pages()

    def get_page(self, url: str) -> Page:
        if url not in self.pages:
            self.add_page(url)
        return self.pages[url]

    def get_all_page_urls(self) -> set[str]:
        return set(self.pages.keys())
