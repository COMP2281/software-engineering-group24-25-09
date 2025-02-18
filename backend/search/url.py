from .types import SearchResult


class URL:
    def __init__(self, data: SearchResult) -> None:
        self.url = data["link"]
        self.title = data["title"]
        self.snippet = data["snippet"]
        self.domain = data["displayLink"]

    def __str__(self) -> str:
        return self.url

    def __hash__(self) -> int:
        return hash(self.url)

    def __eq__(self, other: any) -> bool:
        if isinstance(other, URL):
            return str(self) == str(other)
        else:
            return False
