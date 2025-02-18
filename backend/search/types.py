from typing import TypedDict


class SearchResult(TypedDict):
    title: str
    link: str
    displayLink: str
    snippet: str


class SearchResponse(TypedDict):
    items: list[SearchResult]
