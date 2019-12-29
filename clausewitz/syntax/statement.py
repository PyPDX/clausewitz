import typing as _typing
from tokenize import (
    TokenInfo as _TokenInfo,
)

from .element import (
    Element as _Element,
    String as _String,
    Operator as _Operator,
    Modifier as _Modifier,
)


class Statement(_typing.List[_Element]):
    class End(Exception):
        def __init__(self, reject_last: bool):
            self.reject_last = reject_last

    class Invalid(Exception):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._queue: _Tokens = _Tokens(self)

    def _raise(self, token: _TokenInfo = None):
        if token is not None:
            raise self.Invalid(self, self._queue, token)
        else:
            raise self.Invalid(self, self._queue)

    def finish_queue(self):
        if self._queue:
            self.append(self._queue.value)
            self._queue.clear()

    def _end(self, *, reject_last: bool):
        self.finish_queue()
        raise self.End(reject_last)

    @property
    def accepts_value(self) -> bool:
        return len(self) == 0 or \
               isinstance(self[-1], _Operator) or \
               isinstance(self[-1], _Modifier)

    def push(self, token: _TokenInfo) -> None:
        try:
            self._queue.append(token)

        except self._queue.ShouldNotAppend:
            self.finish_queue()

            if token.exact_type in _Tokens.OPERATORS:
                self.append(_Operator(token.exact_type, token.string))
            elif token.exact_type in _Tokens.START_SCOPE:
                self.append(_Scope())
            elif token.exact_type in _Tokens.STRING_TYPES:
                self.append(_String(token.string))
            else:
                self._raise(token)

        except self._queue.EndStatement:
            if token.exact_type in _Tokens.END_SCOPE:
                return self._end(reject_last=False)
            else:
                return self._end(reject_last=True)

    @property
    def values(self) -> _typing.List:
        return [
            element.value
            for element in self
        ]


from .token import (  # noqa: E402
    Tokens as _Tokens,
)
from .scope import (  # noqa: E402
    Scope as _Scope,
)
