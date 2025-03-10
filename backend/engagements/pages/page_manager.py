from engagements.pages.page import Page
from engagements.saver import Saver


class PageManager(Saver):
    def __init__(self, data_path: str) -> None:
        super().__init__(data_path, "pages")

    def add_page(self, url: str) -> None:
        if url in self.data:
            return
        self.data[url] = Page(url)
        self.save_data()

    def remove_page(self, url: str) -> None:
        del self.data[url]
        self.save_data()

    def update_page(self, url: str) -> None:
        if url not in self.data:
            return
        self.data[url].update()
        self.save_data()

    def get_page(self, url: str) -> Page:
        if url not in self.data:
            self.add_page(url)
        return self.data[url]

    def get_all_page_urls(self) -> set[str]:
        return set(self.data.keys())
