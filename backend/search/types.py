from typing import TypedDict, NotRequired


class SearchResult(TypedDict):
    title: str
    link: str
    displayLink: str
    snippet: NotRequired[str]


class SearchResponse(TypedDict):
    items: list[SearchResult]
