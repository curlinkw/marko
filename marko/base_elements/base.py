from __future__ import annotations

import re
from typing import (
    ClassVar,
    Any,
    Self,
    Literal,
    Annotated,
    Union,
    Optional,
    Iterator,
    Sequence,
    TYPE_CHECKING,
)
from pydantic import Field
from langchain_core.load.serializable import Serializable

from marko.utils import camel_to_snake_case

if TYPE_CHECKING:
    from marko.source import Source
    from marko.inline_parser import _Match


class BaseElement(Serializable):
    """This class holds attributes common to both the BlockElement and
    InlineElement classes.
    This class should not be subclassed by any other classes beside these.
    """

    priority: ClassVar[int]
    """Use to denote the precedence in parsing"""

    virtual: ClassVar[bool]
    """If True, it won't be included in parsing process but \
        produced by other elements other elements instead."""

    override: ClassVar[bool]
    """If true, will replace the element which it derives from."""

    @classmethod
    def initialize(cls, *args, **kwargs) -> Self:
        kwargs = cls.initialize_kwargs(*args, **kwargs)

        private_kwargs = dict()
        for field_name in list(kwargs.keys()):
            if field_name.startswith("_"):
                private_kwargs[field_name] = kwargs.pop(field_name)

        result = cls(**kwargs)

        for name, value in private_kwargs.items():
            setattr(result, name, value)

        return result

    @classmethod
    def initialize_kwargs(cls, *args, **kwargs) -> dict[str, Any]:
        return dict()

    @classmethod
    def get_type(cls, snake_case: bool = False) -> str:
        """
        Return the Markdown element type that the object represents.

        :param snake_case: Return the element type name in snake case if True
        """

        # Prevent override of BlockElement and InlineElement
        if (
            cls.override
            and cls.__base__
            and cls.__base__ not in BaseElement.__subclasses__()
        ):
            name = cls.__base__.__name__
        else:
            name = cls.__name__
        return camel_to_snake_case(name) if snake_case else name

    @classmethod
    def is_lc_serializable(cls) -> bool:
        return True

    def __repr__(self) -> str:
        try:
            from objprint import objstr
        except ImportError:
            from pprint import pformat

            children_repr = (
                f" children={pformat(children)}"
                if hasattr(self, "children")
                and (children := getattr(self, "children")) is not None
                else ""
            )
            return f"<{self.__class__.__name__}{children_repr}>"
        else:
            return objstr(self, honor_existing=False, include=["children"])


class BlockElement(BaseElement):
    """Any block element should inherit this class"""

    priority: ClassVar[int] = 5
    """Default priority"""

    virtual: ClassVar[bool] = False
    """Default: False"""

    override: ClassVar[bool] = False
    """Default: False"""

    element_type: Literal["BlockElement"] = "BlockElement"

    children: Sequence[
        Annotated[
            Union[BlockElement, InlineElement],
            Field(discriminator="element_type"),
        ]
    ] = Field(default_factory=list)
    """An attribute to hold the children"""

    inline_body: str = ""
    """If not empty, the body needs to be parsed as inline elements"""

    _prefix: str = ""

    @classmethod
    def match(cls, source: Source) -> Any:
        """Test if the source matches the element at current position.
        The source should not be consumed in the method unless you have to.

        :param source: the ``Source`` object of the content to be parsed
        """
        raise NotImplementedError()

    @classmethod
    def parse(cls, source: Source) -> Any:
        """Parses the source. This is a proper place to consume the source body and
        return an element or information to build one. The information tuple will be
        passed to ``__init__`` method afterwards. Inline parsing, if any, should also
        be performed here.

        :param source: the ``Source`` object of the content to be parsed
        """
        raise NotImplementedError()

    def __lt__(self, other: BaseElement) -> bool:
        return self.priority < other.priority


class InlineElement(BaseElement):
    """Any inline element should inherit this class"""

    priority: ClassVar[int] = 5
    """Default priority"""

    virtual: ClassVar[bool] = False
    """Default: False"""

    override: ClassVar[bool] = False
    """Default: False"""

    pattern: ClassVar[re.Pattern | str] = ""
    """Element regex pattern."""

    parse_children: ClassVar[bool] = False
    """Whether to parse children."""

    parse_group: ClassVar[int] = 1
    """which match group to parse."""

    element_type: Literal["InlineElement"] = "InlineElement"

    children: Optional[
        Sequence[
            Union[
                str,
                Annotated[
                    Union[BlockElement, InlineElement],
                    Field(discriminator="element_type"),
                ],
            ]
        ]
    ] = None
    """An attribute to hold the children"""

    @classmethod
    def initialize_kwargs(cls, match: _Match) -> dict[str, Any]:
        """Parses the matched object into an element"""
        return {} if cls.parse_children else {"children": match.group(cls.parse_group)}

    @classmethod
    def find(cls, text: str, *, source: Source) -> Iterator[_Match]:
        """This method should return an iterable containing matches of this element."""
        if isinstance(cls.pattern, str):
            cls.pattern = re.compile(cls.pattern)
        return cls.pattern.finditer(text)
