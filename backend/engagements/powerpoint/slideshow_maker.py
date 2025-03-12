import os

from lxml.html.diff import start_tag
from pptx import Presentation
from pptx.slide import Slide
from engagements.powerpoint.engagement_slide import EngagementSlide


class SlideshowMaker:
    def __init__(self, data_path: str) -> None:
        templates_file_path = os.path.join(data_path, "templates.pptx")
        templates_file = open(templates_file_path, "rb")
        self.templates: list[Slide] = [
            slide for slide in Presentation(templates_file).slides
        ]

    def get_template(self, index: int) -> Slide:
        if index >= len(self.templates):
            raise IndexError("Slide index out of range")
        return self.templates[index]

    @staticmethod
    def export(slides: list[EngagementSlide]) -> None:
        presentation = Presentation()
        for slide in slides:
            presentation.slides.append(slide)
        presentation.save("export.pptx")


slideshow_maker = SlideshowMaker(".")
for template in slideshow_maker.templates:
    print(template.shapes)
