import os
from pptx import Presentation
from engagements.powerpoint.slide_builder import SlideBuilder


class SlideshowMaker:
    def __init__(self, data_path: str) -> None:
        templates_file_path = os.path.join(data_path, "templates.pptx")
        templates_file = open(templates_file_path, "rb")
        self.templates = [
            SlideBuilder(slide) for slide in Presentation(templates_file).slides
        ]


slideshow_maker = SlideshowMaker(".")
for template in slideshow_maker.templates:
    print(template.shapes)
