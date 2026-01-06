"""
Base parser
"""

from __future__ import annotations

from marko.markdown_spec import MarkdownSpec
from marko.base_elements import BlockElement, Document, RawText
from marko.source import Source, parse_source
from marko.inline_parser import parse_inline


def parse(self, text: str, spec: MarkdownSpec) -> Document:
    """Do the actual parsing and returns an AST or parsed element.

    :param text: the text to parse.
    :returns: the parsed root element
    """
    source = Source(text, spec=spec)
    doc = Document()
    with source.under_state(doc):
        doc.children = parse_source(source)
        element_parse_inline(element=doc, source=source)
    return doc


def element_parse_inline(element: BlockElement, source: Source) -> None:
    """Inline parsing is postponed so that all link references
    are seen before that.
    """
    if element.inline_body:
        element.children = parse_inline(
            text=element.inline_body, fallback=RawText, source=source
        )
        # clear the inline body to avoid parsing it again.
        element.inline_body = ""
    else:
        for child in element.children:
            if isinstance(child, BlockElement):
                element_parse_inline(element=child, source=source)
