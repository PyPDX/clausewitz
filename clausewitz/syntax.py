import abc as _abc
import tokenize as _tokenize
import typing as _typing
from tokenize import (
    TokenInfo as _TokenInfo,
)

from cached_property import cached_property
from returns import (
    returns as _returns,
)

from .datastructure import (
    Dict as _Dict,
)
from .strings import (
    unescape as _unescape,
)


class Element(_abc.ABC):
    @property
    @_abc.abstractmethod
    def value(self):
        raise NotImplementedError  # pragma: no cover

    def __eq__(self, other):
        return self.value == other


class Name(Element):
    def __init__(self, raw: str):
        self._raw = raw

    @property
    def value(self):
        return self._raw


class Number(Element):
    def __init__(self, neg: bool, raw: str):
        self._neg = neg
        self._raw = raw

    @property
    def raw_string(self) -> str:
        return ('-' if self._neg else '') + self._raw

    @cached_property
    def value(self):
        s = self.raw_string
        if '.' in s:
            return float(s)
        else:
            return int(s)


class String(Element):
    def __init__(self, raw: str):
        self._raw = raw

    @property
    def raw_string(self) -> str:
        return self._raw

    @cached_property
    def value(self):
        return _unescape(self.raw_string)


class Operator(Element):
    def __init__(self, exact_type: int, raw: str):
        self._exact_type = exact_type
        self._raw = raw

    @cached_property
    def value(self):
        return self._raw


class Scope(Element):
    class SerializationError(Exception):
        def __init__(self, data=None):
            from pprint import pformat
            super().__init__(pformat(data))
            self.data = data

    def __init__(self):
        self._statements: _typing.List['Statement'] = []
        self._current_statement: _typing.Optional['Statement'] = None

    @property
    def current_statement(self) -> 'Statement':
        if self._current_statement is None:
            self._current_statement = Statement()
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
                if token.exact_type == _tokenize.RBRACE and len(self._statements) == 0:
                    return

                try:
                    self.current_statement.push(token)
                except Statement.End as end:
                    self.finish_statement()
                    if end.reject_last:
                        self.current_statement.push(token)

                if token.exact_type == _tokenize.LBRACE:
                    scope: Scope = self.current_statement[-1]
                    scope.push(tokens)

                elif token.exact_type == _tokenize.RBRACE:
                    return

        finally:
            self.finish_statement()


class _StatementQueue(_typing.List[_TokenInfo]):
    class ShouldNotAppend(Exception):
        pass

    class EndStatement(Exception):
        pass

    def __init__(self, parent: 'Statement'):
        super().__init__()
        self._parent = parent

    def append(self, token: _TokenInfo):
        if token.exact_type in Statement.OPS:
            raise self.ShouldNotAppend

        if token.exact_type in (
                _tokenize.RBRACE,
        ):
            raise self.EndStatement

        if token.exact_type in (
                _tokenize.LBRACE,
                _tokenize.STRING,
        ):
            if self:
                raise self.EndStatement

            else:
                if self._parent.last_op:
                    raise self.ShouldNotAppend
                else:
                    raise self.EndStatement

        if self:
            if self[-1].end != token.start:
                raise self.EndStatement

        else:
            if not self._parent.last_op:
                raise self.EndStatement

        super().append(token)

    @property
    def number(self) -> _typing.Optional[Number]:
        if not self:
            return None

        elif len(self) == 1:
            if self[0].type != _tokenize.NUMBER:
                return None
            return Number(False, self[0].string)

        elif len(self) == 2:
            if not (self[0].exact_type == _tokenize.MINUS and
                    self[1].type == _tokenize.NUMBER):
                return None
            return Number(True, self[1].string)

        else:
            return None

    @property
    def name(self) -> Name:
        return Name(''.join(
            token.string
            for token in self
        ))

    @property
    def value(self) -> Element:
        return self.number or self.name


class Statement(_typing.List[Element]):
    OPS = (
        _tokenize.EQUAL,
        _tokenize.LESS,
        _tokenize.LESSEQUAL,
        _tokenize.GREATER,
        _tokenize.GREATEREQUAL,
    )

    class End(Exception):
        def __init__(self, reject_last: bool):
            self.reject_last = reject_last

    class Invalid(Exception):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._queue: _StatementQueue = _StatementQueue(self)

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
    def last_op(self) -> bool:
        return len(self) == 0 or isinstance(self[-1], Operator)

    def push(self, token: _TokenInfo) -> None:
        try:
            self._queue.append(token)

        except self._queue.ShouldNotAppend:
            self.finish_queue()

            if token.exact_type in self.OPS:
                self.append(Operator(token.exact_type, token.string))
            elif token.exact_type == _tokenize.LBRACE:
                self.append(Scope())
            elif token.exact_type == _tokenize.STRING:
                self.append(String(token.string))
            else:
                self._raise(token)

        except self._queue.EndStatement:
            if token.exact_type == _tokenize.RBRACE:
                return self._end(reject_last=False)
            else:
                return self._end(reject_last=True)
