import abc as _abc

from cached_property import cached_property

from ..util.strings import (
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
        return _unescape(self.raw_string[2:-2])


class Operator(Element):
    def __init__(self, exact_type: int, raw: str):
        self._exact_type = exact_type
        self._raw = raw

    @property
    def value(self):
        return self._raw


class Modifier(Element):
    MODIFIERS = (
        'rgb',
        'hsv',
    )

    def __init__(self, raw: str):
        self._raw = raw

    @property
    def value(self):
        return self._raw
