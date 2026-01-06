from typing import Type, TypeAlias, Union

from marko.base_elements.base import BaseElement, BlockElement, InlineElement


BaseElementType = Type[BaseElement]
BlockElementType = Type[BlockElement]
InlineElementType = Type[InlineElement]
Element: TypeAlias = Union[BlockElement, InlineElement]
