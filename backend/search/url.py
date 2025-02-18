from .types import SearchResult


class URL:
    def __init__(self, data: SearchResult) -> None:
        self.url = data["link"]
        self.title = data["title"]
        self.snippet = data["snippet"]
        self.domain = data["displayLink"]

    def __str__(self) -> str:
        return self.url
