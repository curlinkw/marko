from typing import ClassVar, Any

from marko.base_elements.base import InlineElement


class RawText(InlineElement):
    """The raw text is the fallback for all holes that doesn't match any others."""

    virtual: ClassVar[bool] = True

    escape: bool

    @classmethod
    def initialize_kwargs(cls, match: str, escape: bool = True) -> dict[str, Any]:  # type: ignore[override]
        return {
            "children": match,
            "escape": escape,
        }
