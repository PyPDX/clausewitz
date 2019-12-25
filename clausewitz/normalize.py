from cached_property import cached_property
from logical.collection import In


class Normalizer(object):
    TOKENS = ('=',)

    def __init__(
            self,
            *,
            tokens=None,
    ):
        self.__tokens = tokens

    @cached_property
    def _is_token_func(self):
        tokens = self.__tokens
        if tokens is None:
            tokens = self.TOKENS
        if not callable(tokens):
            tokens = In(tokens)
        return tokens

    def is_token(self, val):
        return self._is_token_func(val)

    def normalize(self, val):
        if not isinstance(val, list):
            return val

        if all(
                len(item) == 1
                for item in val
        ):
            return [
                self.normalize(item[0])
                for item in val
            ]

        if all(
                len(item) == 3 and self.is_token(item[1])
                for item in val
        ):
            return {
                item[0]: self.normalize(item[2])
                for item in val
            }

        raise ValueError(val)
