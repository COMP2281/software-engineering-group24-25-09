import os
from enum import Enum
from pptx import Presentation
from pptx.shapes.autoshape import Shape
from pptx.slide import Slide
from typing import cast


class ShapeType(Enum):
    TITLE = "TITLE"
    SUMMARY = "SUMMARY"
    EMPLOYEES = "EMPLOYEES"


class SlideTemplate:
    @staticmethod
    def _find_shapes(template: Slide) -> dict[ShapeType, int]:
        shapes = {}
        for shape in template.shapes:
            shape: Shape
            if shape.has_text_frame and shape.text in ShapeType:
                shape_type = cast(ShapeType, ShapeType[shape.text])
                shapes[shape_type] = shape.shape_id
        return shapes

    def __init__(self, template: Slide) -> None:
        self.template = template
        self.shapes = self._find_shapes(template)


class SlideshowMaker:
    def __init__(self, data_path: str) -> None:
        templates_file_path = os.path.join(data_path, "templates.pptx")
        templates_file = open(templates_file_path, "rb")
        self.templates = [
            SlideTemplate(slide) for slide in Presentation(templates_file).slides
        ]


slideshow_maker = SlideshowMaker(".")
print(slideshow_maker.templates)
