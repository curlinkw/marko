from typing import cast, Any

from marko._import_utils import import_attr
from marko.elements.base import BaseElement
from marko.elements.inline import InlineElement
from marko.elements.block import BlockElement


block_elements = [
    "Document",
    "CodeBlock",
    "Heading",
    "List",
    "ListItem",
    "BlankLine",
    "Quote",
    "FencedCode",
    "ThematicBreak",
    "HTMLBlock",
    "LinkRefDef",
    "SetextHeading",
    "Paragraph",
]

inline_elements = [
    "LineBreak",
    "Literal",
    "InlineHTML",
    "CodeSpan",
    "Emphasis",
    "StrongEmphasis",
    "Link",
    "Image",
    "AutoLink",
    "RawText",
]


def _import_elements(module, elements: list[str]) -> dict[str, Any]:
    return {
        (
            element := cast(
                BaseElement,
                import_attr(
                    attr_name=element_name, module_name=module, package=__spec__.name
                ),
            )
        ).get_type(): element
        for element_name in elements
    }


COMMON_INLINE_ELEMENTS: dict[str, InlineElement] = _import_elements(
    "inline", inline_elements
)
COMMON_BLOCK_ELEMENTS: dict[str, BlockElement] = _import_elements(
    "block", block_elements
)

__all__ = [
    "COMMON_INLINE_ELEMENTS",
    "COMMON_BLOCK_ELEMENTS",
    "BaseElement",
    "BlockElement",
    "InlineElement",
]
