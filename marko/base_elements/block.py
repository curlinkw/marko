from typing import ClassVar
from pydantic import Field
from marko.base_elements.base import BlockElement


class Document(BlockElement):
    """Document node element."""

    virtual: ClassVar[bool] = True

    link_ref_defs: dict[str, tuple[str, str]] = Field(default_factory=dict)
