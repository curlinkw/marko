"""
Helper functions and data structures
"""

from __future__ import annotations

from importlib import import_module
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Type, Any


class MarkoExtension(BaseModel):
    parser_mixins: List[Type] = Field(default_factory=list)
    renderer_mixins: List[Type] = Field(default_factory=list)

    elements: List[Type] = Field(default_factory=list)
    # must be Type[Element], but tests use as Any

    model_config = ConfigDict(frozen=True, extra="forbid")


def load_extension(name: str, **kwargs: Any) -> MarkoExtension:
    """Load extension object from a string.
    First try `marko.ext.<name>` if possible
    """
    module = None
    if "." not in name:
        try:
            module = import_module(f"marko.ext.{name}")
        except ImportError:
            pass
    if module is None:
        try:
            module = import_module(name)
        except ImportError as e:
            raise ImportError(f"Extension {name} cannot be imported") from e

    try:
        return module.make_extension(**kwargs)
    except AttributeError:
        raise AttributeError(
            f"Module {name} does not have 'make_extension' attributte."
        ) from None
