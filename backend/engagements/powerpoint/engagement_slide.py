from typing import cast, Self
from bs4 import BeautifulSoup
from pptx.shapes.placeholder import LayoutPlaceholder
from pptx.slide import SlideLayout
from engagements.powerpoint.types import PlaceholderType, PlaceholderDataType


class EngagementSlide:
    def _set_placeholders(self):
        self.placeholders = {}
        if not self.layout:
            raise Exception("Missing layout")
        for placeholder in self.layout.placeholders:
            placeholder: LayoutPlaceholder
            if placeholder.has_text_frame and placeholder.text in PlaceholderType:
                self.placeholders[
                    cast(PlaceholderType, PlaceholderType[placeholder.text])
                ] = placeholder.placeholder_format.idx

    def reset(self, layout: SlideLayout) -> Self:
        self.layout = layout
        self._set_placeholders()
        return self

    def __init__(self, layout: SlideLayout) -> None:
        self.layout: SlideLayout | None = None
        self.placeholders: dict[PlaceholderType, int] = {}
        self.placeholder_values: dict[PlaceholderType, PlaceholderDataType]
        self.reset(layout)

    def get_layout(self) -> SlideLayout:
        return self.layout

    @property
    def title(self) -> str:
        return self.title

    @title.setter
    def title(self, title: str) -> None:
        self.title = title

    @property
    def summary(self) -> list[str]:
        return self.summary

    @summary.setter
    def summary(self, summary: list[str]) -> None:
        self.summary = summary

    @property
    def employees(self) -> list[str]:
        return self.employees

    @employees.setter
    def employees(self, employees: list[str]) -> None:
        self.employees = employees

    @property
    def image(self) -> str:
        return self.image

    @image.setter
    def image(self, image: BeautifulSoup) -> None:
        # TODO: handle srcset attribute
        self.image = image["src"]

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
