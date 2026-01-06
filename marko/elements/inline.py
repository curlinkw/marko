"""
Inline(span) level elements
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, ClassVar, Optional, Any

from marko import patterns
from marko.base_elements import InlineElement, RawText

if TYPE_CHECKING:
    from marko.inline_parser import _Match


class Literal(InlineElement):
    """Literal escapes need to be parsed at the first."""

    priority: ClassVar[int] = 7
    pattern: ClassVar[re.Pattern | str] = re.compile(
        r'\\([!"#\$%&\'()*+,\-./:;<=>?@\[\\\]^_`{|}~])'
    )

    @classmethod
    def strip_backslash(cls, text: str) -> str:
        return cls.pattern.sub(r"\1", text)  # type: ignore[unio]


class LineBreak(InlineElement):
    """Line breaks:

    Soft: '\n'
    Hard: '  \n'
    """

    priority: ClassVar[int] = 2
    pattern: ClassVar[re.Pattern | str] = r"( *|\\)\n(?!\Z)"

    soft: bool

    @classmethod
    def initialize_kwargs(cls, match: _Match) -> dict[str, Any]:
        return {
            "soft": not match.group(1).startswith(("  ", "\\")),
            "children": "\n",
        }


class InlineHTML(InlineElement):
    priority: ClassVar[int] = 7
    pattern: ClassVar[re.Pattern | str] = re.compile(
        r"(<%s(?:%s)* */?>"  # open tag
        r"|</%s *>"  # closing tag
        r"|<!--(?:>|->|[\s\S]*?-->)"  # HTML comment
        r"|<\?[\s\S]*?\?>"  # processing instruction
        r"|<![A-Z]+ +[\s\S]*?>"  # declaration
        r"|<!\[CDATA\[[\s\S]*?\]\]>)"  # CDATA section
        % (patterns.tag_name, patterns.attribute, patterns.tag_name)
    )


class StrongEmphasis(InlineElement):
    """Strong emphasis: **sample text**"""

    virtual: ClassVar[bool] = True
    parse_children: ClassVar[bool] = True


class Emphasis(InlineElement):
    """Emphasis: *sample text*"""

    virtual: ClassVar[bool] = True
    parse_children: ClassVar[bool] = True


class Link(InlineElement):
    """Link: [text](/link/destination)"""

    virtual: ClassVar[bool] = True
    parse_children: ClassVar[bool] = True

    dest: str
    title: Optional[str]

    @classmethod
    def initialize_kwargs(cls, match: _Match) -> dict[str, Any]:
        if match.group(2) and match.group(2)[0] == "<" and match.group(2)[-1] == ">":
            _dest = match.group(2)[1:-1]
        else:
            _dest = match.group(2) or ""
        return {
            "dest": Literal.strip_backslash(_dest),
            "title": (
                Literal.strip_backslash(match.group(3)[1:-1])
                if match.group(3)
                else None
            ),
        }


class Image(InlineElement):
    """Image: ![alt](/src/address)"""

    virtual: ClassVar[bool] = True
    parse_children: ClassVar[bool] = True

    dest: str
    title: Optional[str]

    @classmethod
    def initialize_kwargs(cls, match: _Match) -> dict[str, Any]:
        if match.group(2) and match.group(2)[0] == "<" and match.group(2)[-1] == ">":
            _dest = match.group(2)[1:-1]
        else:
            _dest = match.group(2) or ""
        return {
            "dest": Literal.strip_backslash(_dest),
            "title": (
                Literal.strip_backslash(match.group(3)[1:-1])
                if match.group(3)
                else None
            ),
        }


class CodeSpan(InlineElement):
    """Inline code span: `code sample`"""

    priority: ClassVar[int] = 7
    pattern: ClassVar[re.Pattern | str] = re.compile(
        r"(?<!`)(`+)(?!`)([\s\S]+?)(?<!`)\1(?!`)"
    )

    @classmethod
    def initialize_kwargs(cls, match: _Match) -> dict[str, Any]:
        _children = match.group(2).replace("\n", " ")
        if _children.strip() and _children[0] == _children[-1] == " ":
            _children = _children[1:-1]
        return {
            "children": _children,
        }


class AutoLink(InlineElement):
    """Autolinks: <http://example.org>"""

    priority: ClassVar[int] = 7
    pattern: ClassVar[re.Pattern | str] = re.compile(
        rf"<({patterns.uri}|{patterns.email})>"
    )

    dest: str
    title: Optional[str]

    @classmethod
    def initialize_kwargs(cls, match: _Match) -> dict[str, Any]:
        _dest = match.group(1)
        if re.match(patterns.email, _dest):
            _dest = "mailto:" + _dest
        return {
            "children": [RawText.initialize(match.group(1))],
            "title": "",
            "dest": _dest,
        }
