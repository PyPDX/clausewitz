import tokenize as _tokenize
import typing as _typing
from tokenize import (
    TokenInfo as _TokenInfo,
)

from .element import (
    Element as _Element,
    Number as _Number,
    Name as _Name,
)


class Tokens(_typing.List[_TokenInfo]):
    START_SCOPE = (
        _tokenize.LBRACE,
    )
    END_SCOPE = (
        _tokenize.RBRACE,
    )

    OPERATORS = (
        _tokenize.EQUAL,
        _tokenize.LESS,
        _tokenize.LESSEQUAL,
        _tokenize.GREATER,
        _tokenize.GREATEREQUAL,
    )

    STRING_TYPES = (
        _tokenize.STRING,
    )

    @property
    def number(self) -> _typing.Optional['_Number']:
        if not self:
            return None

        elif len(self) == 1:
            if self[0].type != _tokenize.NUMBER:
                return None
            return _Number(False, self[0].string)

        elif len(self) == 2:
            if not (self[0].exact_type == _tokenize.MINUS and
                    self[1].type == _tokenize.NUMBER):
                return None
            return _Number(True, self[1].string)

        else:
            return None

    @property
    def name(self) -> '_Name':
        return _Name(''.join(
            token.string
            for token in self
        ))

    class ShouldNotAppend(Exception):
        pass

    class EndStatement(Exception):
        pass

    def __init__(self, parent: '_Statement'):
        super().__init__()
        self._parent = parent

    def append(self, token: _TokenInfo):
        if token.exact_type in self.OPERATORS:
            raise self.ShouldNotAppend

        if token.exact_type in self.END_SCOPE:
            raise self.EndStatement

        if token.exact_type in (
                *self.START_SCOPE,
                *self.STRING_TYPES,
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
    def value(self) -> '_Element':
        return self.number or self.name


from .statement import (  # noqa: E402
    Statement as _Statement,
)
