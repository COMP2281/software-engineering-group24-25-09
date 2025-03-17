from enum import Enum
from typing import TypeAlias


class PlaceholderType(Enum):
    TITLE = "TITLE"
    SUMMARY = "SUMMARY"
    EMPLOYEES = "EMPLOYEES"
    IMAGE = "IMAGE"


PlaceholderDataType: TypeAlias = str | list[str]
