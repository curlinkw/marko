from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, overload, cast

from marko.renderers import BaseRenderer

if TYPE_CHECKING:
    from marko.base_elements.base import BaseElement
    from typing import Any, Callable, TypeVar

    RendererFunc = Callable[[Any, BaseElement], Any]
    TRenderer = TypeVar("TRenderer", bound=RendererFunc)


class _RendererDispatcher:
    name: str

    def __init__(
        self,
        types: type[BaseRenderer] | tuple[type[BaseRenderer], ...],
        func: RendererFunc,
    ) -> None:
        from marko.renderers.ast_renderer import ASTRenderer, XMLRenderer

        self._mapping = {types: func}
        self._mapping.setdefault((ASTRenderer, XMLRenderer), self.render_ast)

    def dispatch(
        self: _RendererDispatcher,
        types: type[BaseRenderer] | tuple[type[BaseRenderer], ...],
    ) -> Callable[[RendererFunc], _RendererDispatcher]:
        def decorator(func: RendererFunc) -> _RendererDispatcher:
            self._mapping[types] = func
            return self

        return decorator

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    @staticmethod
    def render_ast(self, element: BaseElement) -> Any:
        return self.render_children(element)

    def super_render(self, r: Any, element: BaseElement) -> Any:
        """Call on the next class in the MRO which has the same method."""
        klasses = (c for c in type(r).mro() if self.name in c.__dict__)
        try:
            next(klasses)  # skip the current class
            parent = next(klasses)
        except StopIteration:
            raise NotImplementedError(f"Unsupported renderer {type(r)}") from None
        else:
            return getattr(parent, self.name)(r, element)

    @overload
    def __get__(
        self: _RendererDispatcher, obj: None, owner: type
    ) -> _RendererDispatcher: ...

    @overload
    def __get__(
        self: _RendererDispatcher, obj: BaseRenderer, owner: type
    ) -> RendererFunc: ...

    def __get__(
        self: _RendererDispatcher, obj: BaseRenderer | None, owner: type
    ) -> RendererFunc | _RendererDispatcher:
        if obj is None:
            return self
        for types, func in self._mapping.items():
            if isinstance(obj, types):
                return cast(RendererFunc, partial(func, obj))
        return cast(RendererFunc, partial(self.super_render, obj))


def render_dispatch(
    types: type[BaseRenderer] | tuple[type[BaseRenderer], ...],
) -> Callable[[RendererFunc], _RendererDispatcher]:
    def decorator(func: RendererFunc) -> _RendererDispatcher:
        return _RendererDispatcher(types, func)

    return decorator
