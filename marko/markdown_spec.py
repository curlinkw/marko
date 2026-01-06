from dataclasses import dataclass, field

from marko.base_elements import (
    BlockElementType,
    InlineElementType,
)


@dataclass(frozen=True)
class MarkdownSpec:
    """Markdown specification."""

    block_elements: dict[str, BlockElementType] = field(default_factory=dict)
    """Block elements: give only custom ones."""
    inline_elements: dict[str, InlineElementType] = field(default_factory=dict)
    """Inline elements: give only custom ones."""

    @property
    def non_virtual_block_elements(self) -> list[BlockElementType]:
        """Return a list of non-virtual block elements, ordered from highest priority to lowest."""
        return sorted(
            (e for e in self.block_elements.values() if not e.virtual),
            key=lambda e: e.priority,
            reverse=True,
        )

    @property
    def non_virtual_inline_elements(self) -> list[InlineElementType]:
        """Return a list of non-virtual inline elements."""
        return [e for e in self.inline_elements.values() if not e.virtual]
