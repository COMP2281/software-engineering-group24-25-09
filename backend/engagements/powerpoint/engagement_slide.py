from copy import deepcopy
from pptx.shapes.autoshape import Shape
from pptx.slide import Slide
from typing import cast, Callable
from engagements.powerpoint.shape_type import ShapeType


class EngagementSlide:
    @staticmethod
    def _create_set_text_shape(template: Slide) -> Callable[[ShapeType, str], None]:
        text_shapes = {}
        for shape in template.shapes:
            shape: Shape
            if shape.has_text_frame and shape.text in ShapeType:
                shape_type = cast(ShapeType, ShapeType[shape.text])
                text_shapes[shape_type] = shape

        def set_text_shape(shape_type: ShapeType, value: str):
            if shape_type not in text_shapes:
                return
            text_shapes[shape_type].text = value

        return set_text_shape

    def reset(self, template: Slide) -> None:
        self.slide = deepcopy(template)
        self.set_text_shape = self._create_set_text_shape(template)

    def __init__(self, template: Slide) -> None:
        self.slide: Slide | None = None
        self.set_text_shape: Callable[[ShapeType, str], None] | None = None
        self.reset(template)

    def set_title(self, title: str) -> None:
        self.set_text_shape(ShapeType.TITLE, title)

    def set_summary(self, summary: str) -> None:
        self.set_text_shape(ShapeType.SUMMARY, summary)

    def set_employees(self, employees: str) -> None:
        self.set_text_shape(ShapeType.EMPLOYEES, employees)
