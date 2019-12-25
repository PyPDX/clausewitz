from .abstract import AbstractNodeReader


class AbstractStringReader(AbstractNodeReader):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._result = ''

    def _read(self, c):
        self._result += c

    @property
    def result(self):
        return self._result


class StringReader(AbstractStringReader):
    START = '"'
    END = '"'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._escaping = False

    def _read(self, c):
        if c != '\\':
            self._escaping = False
        else:
            self._escaping = not self._escaping
        super()._read(c)

    def end(self, c):
        return not self._escaping and super().end(c)


class CommentReader(AbstractStringReader):
    START = '#'
    END = '\n'
