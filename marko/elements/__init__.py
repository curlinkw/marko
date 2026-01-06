from typing import cast, Any

from marko._import_utils import import_attr
from marko.base_elements import (
    BaseElement,
    BlockElementType,
    InlineElementType,
)
from marko.elements.block import (
    CodeBlock,
    Heading,
    List,
    ListItem,
    BlankLine,
    Quote,
    FencedCode,
    ThematicBreak,
    HTMLBlock,
    LinkRefDef,
    SetextHeading,
    Paragraph,
)
from marko.elements.inline import (
    LineBreak,
    Literal,
    InlineHTML,
    CodeSpan,
    Emphasis,
    StrongEmphasis,
    Link,
    Image,
    AutoLink,
)


def _import_elements(
    elements: list[str], module: str | None = None, package: str | None = None
) -> dict[str, Any]:
    return {
        (
            element := cast(
                BaseElement,
                import_attr(
                    attr_name=element_name, module_name=module, package=package
                ),
            )
        ).get_type(): element
        for element_name in elements
    }


COMMON_BLOCK_ELEMENTS: dict[str, BlockElementType] = _import_elements(
    elements=[
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
    ],
    module="block",
    package=__spec__.name,
) | _import_elements(elements=["Document"], module="base_elements", package="marko")

COMMON_INLINE_ELEMENTS: dict[str, InlineElementType] = _import_elements(
    elements=[
        "LineBreak",
        "Literal",
        "InlineHTML",
        "CodeSpan",
        "Emphasis",
        "StrongEmphasis",
        "Link",
        "Image",
        "AutoLink",
    ],
    module="inline",
    package=__spec__.name,
) | _import_elements(elements=["RawText"], module="base_elements", package="marko")

__all__ = [
    "COMMON_INLINE_ELEMENTS",
    "COMMON_BLOCK_ELEMENTS",
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
    "LineBreak",
    "Literal",
    "InlineHTML",
    "CodeSpan",
    "Emphasis",
    "StrongEmphasis",
    "Link",
    "Image",
    "AutoLink",
]
