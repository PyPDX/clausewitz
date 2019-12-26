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
        pass

    def __init__(self):
        self._statements: _typing.List['Statement'] = []
        self._current_statement = None

    @property
    def current_statement(self) -> 'Statement':
        if self._current_statement is None:
            self._current_statement = Statement()
            self._statements.append(self._current_statement)
        return self._current_statement

    def finish_statement(self) -> None:
        self._current_statement = None

    @_returns(list)
    def _as_list(self):
        for statement in self._statements:
            if len(statement) != 1:
                raise self.SerializationError
            yield statement[0].value

    @_returns(dict)
    def _as_dict(self):
        for statement in self._statements:
            if len(statement) != 3:
                raise self.SerializationError
            op = statement[1]
            if not isinstance(op, Operator):
                raise self.SerializationError
            if op != '=':
                raise self.SerializationError
            yield statement[0].value, statement[2].value

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
            return self._as_list()
        except self.SerializationError:
            pass

        try:
            return self._as_dict()
        except self.SerializationError:
            pass

        raise self.SerializationError(self._raw())

    def push(self, tokens: _typing.Iterable[_TokenInfo]):
        tokens = iter(tokens)

        for token in tokens:
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


class Statement(_typing.List[Element]):
    class End(Exception):
        def __init__(self, reject_last: bool):
            self.reject_last = reject_last

    class Invalid(Exception):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._queue: _typing.List[_TokenInfo] = []

    def _raise(self, token: _TokenInfo = None):
        if token is not None:
            raise self.Invalid(self, self._queue, token)
        else:
            raise self.Invalid(self, self._queue)

    def _end(self, *, reject_last: bool):
        if self._queue:
            if self._neg:
                return self._raise()
            elif self._name:
                self.append(Name(self._queue[0].string))
            elif self._name_dot:
                return self._raise()
            else:
                return self._raise()
        raise self.End(reject_last)

    @property
    def last_op(self) -> bool:
        return len(self) == 0 or isinstance(self[-1], Operator)

    @property
    def _neg(self) -> bool:
        return len(self._queue) == 1 and \
               self._queue[0].exact_type == _tokenize.MINUS

    @property
    def _name(self) -> bool:
        return len(self._queue) == 1 and \
               self._queue[0].type == _tokenize.NAME

    @property
    def _name_dot(self) -> bool:
        return len(self._queue) == 2 and \
               self._queue[0].type == _tokenize.NAME and \
               self._queue[1].exact_type == _tokenize.DOT

    def push(self, token: _TokenInfo) -> None:
        if self._queue:
            if self._neg:
                if token.type != _tokenize.NUMBER:
                    return self._raise(token)
                self.append(Number(True, token.string))

            elif self._name:
                if token.type == _tokenize.NUMBER and token.string.startswith('.'):
                    self.append(Name(self._queue[0].string + token.string))

                elif token.exact_type == _tokenize.DOT:
                    self._queue.append(token)
                    return

                else:
                    self.append(Name(self._queue[0].string))
                    self._queue = []
                    return self.push(token)

            elif self._name_dot:
                if token.type != _tokenize.NAME:
                    return self._raise(token)
                self.append(Name(self._queue[0].string + self._queue[1].string + token.string))

            else:
                return self._raise(token)

            self._queue = []
            return

        if not self.last_op:
            if token.type != _tokenize.OP:
                return self._end(reject_last=True)
            if token.exact_type == _tokenize.RBRACE:
                return self._end(reject_last=False)
            if token.exact_type == _tokenize.LBRACE:
                return self._end(reject_last=True)
            self.append(Operator(token.exact_type, token.string))
            return

        if token.type == _tokenize.OP:
            if token.exact_type == _tokenize.MINUS:
                self._queue.append(token)
                return
            if token.exact_type == _tokenize.LBRACE:
                self.append(Scope())
                return
            return self._raise(token)  # two operators

        if token.type == _tokenize.NAME:
            self._queue.append(token)
        elif token.type == _tokenize.NUMBER:
            self.append(Number(False, token.string))
        elif token.type == _tokenize.STRING:
            self.append(String(token.string))
        else:
            return self._raise(token)  # invalid type
