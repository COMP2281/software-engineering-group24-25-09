from typing import Self
from bs4 import BeautifulSoup
from engagements.powerpoint.types import PlaceholderType, PlaceholderDataType


class EngagementSlide:
    def __init__(self) -> None:
        self.layout_index = 0
        self.values: dict[PlaceholderType, PlaceholderDataType] = {}

    @property
    def title(self) -> str | None:
        return self.values.get(PlaceholderType.TITLE)

    @title.setter
    def title(self, title: str) -> None:
        self.values[PlaceholderType.TITLE] = title

    @property
    def summary(self) -> list[str] | None:
        return self.values.get(PlaceholderType.SUMMARY)

    @summary.setter
    def summary(self, summary: list[str]) -> None:
        self.values[PlaceholderType.SUMMARY] = summary

    @property
    def employees(self) -> list[str] | None:
        return self.values.get(PlaceholderType.EMPLOYEES)

    @employees.setter
    def employees(self, employees: list[str]) -> None:
        self.values[PlaceholderType.EMPLOYEES] = employees

    @property
    def image(self) -> str | None:
        return self.values.get(PlaceholderType.IMAGE)

    @image.setter
    def image(self, image: BeautifulSoup) -> None:
        # TODO: handle srcset attribute
        self.values[PlaceholderType.IMAGE] = image["src"]

    def set_title(self, title: str) -> Self:
        self.title = title
        return self

    def set_summary(self, summary: list[str]) -> Self:
        self.summary = summary
        return self

    def set_employees(self, employees: list[str]) -> Self:
        self.employees = employees
        return self

    def set_image(self, image: BeautifulSoup) -> Self:
        self.image = image
        return self

    def set_layout_index(self, index: int) -> Self:
        self.layout_index = index
        return self
