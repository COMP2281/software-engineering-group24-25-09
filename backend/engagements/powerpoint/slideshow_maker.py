import os
from enum import Enum
from pptx import Presentation
from pptx.slide import Slide


class ShapeType(Enum):
    TITLE = "TITLE"
    SUMMARY = "SUMMARY"
    EMPLOYEES = "EMPLOYEES"


class SlideshowMaker:
    def __init__(self, data_path: str) -> None:
        templates_file_path = os.path.join(data_path, "templates.pptx")
        templates_file = open(templates_file_path, "rb")
        self.templates: list[Slide] = [slide for slide in Presentation(templates_file).slides]

slideshow_maker = SlideshowMaker(".")
print(slideshow_maker.templates)
