import typing as _typing
from tokenize import (
    TokenInfo as _TokenInfo,
)

from cached_property import cached_property
from returns import (
    returns as _returns,
)

from .element import (
    Element,
    Operator,
)
from ..datastructure import (
    Dict as _Dict,
)


class Scope(Element):
    class SerializationError(Exception):
        def __init__(self, data=None):
            from pprint import pformat
            super().__init__(pformat(data))
            self.data = data

    def __init__(self):
        self._statements: _typing.List['_Statement'] = []
        self._current_statement: _typing.Optional['_Statement'] = None

    @property
    def current_statement(self) -> '_Statement':
        if self._current_statement is None:
            self._current_statement = _Statement()
            self._statements.append(self._current_statement)
        return self._current_statement

    def finish_statement(self) -> None:
        if self._current_statement is not None:
            self._current_statement.finish_queue()
            self._current_statement = None

    @_returns(list)
    def _as_list(self):
        for statement in self._statements:
            if len(statement) != 1:
                raise self.SerializationError
            yield statement[0].value

    @_returns(_Dict)
    def _as_dict(self):
        for statement in self._statements:
            if len(statement) != 3:
                raise self.SerializationError
            op = statement[1]
            if not isinstance(op, Operator):
                raise self.SerializationError
            yield statement[0].value, (statement[1].value, statement[2].value)

    @_returns(tuple)
    def _raw(self):
        for statement in self._statements:
            yield tuple(
                element.value
                for element in statement
            )

    @cached_property
    def value(self):
        try:
            return self._as_dict()
        except self.SerializationError:
            pass

        try:
            return self._as_list()
        except self.SerializationError:
            pass

        raise self.SerializationError(self._raw())

    def push(self, tokens: _typing.Iterable[_TokenInfo]):
        tokens = iter(tokens)

        try:
            for token in tokens:
                if token.exact_type in _Tokens.END_SCOPE and len(self._statements) == 0:
                    return

                try:
                    self.current_statement.push(token)
                except _Statement.End as end:
                    self.finish_statement()
                    if end.reject_last:
                        self.current_statement.push(token)

                if token.exact_type in _Tokens.START_SCOPE:
                    scope: Scope = self.current_statement[-1]
                    scope.push(tokens)

                elif token.exact_type in _Tokens.END_SCOPE:
                    return

        finally:
            self.finish_statement()


from .token import (  # noqa: E402
    Tokens as _Tokens,
)
from .statement import (  # noqa: E402
    Statement as _Statement,
)
