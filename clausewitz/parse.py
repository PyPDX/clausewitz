import tokenize as _tokenize
import typing as _typing
from tokenize import (
    TokenInfo as _TokenInfo,
)

from clausewitz.syntax.scope import (
    Scope as _Scope,
)


class ErrorToken(Exception):
    pass


class Unfinished(Exception):
    pass


def filter_tokens(tokens: _typing.Iterable[_TokenInfo]) -> _typing.Iterator[_TokenInfo]:
    for token in tokens:
        if token.type in (
                _tokenize.ENCODING,
                _tokenize.NEWLINE,
                _tokenize.NL,
                _tokenize.COMMENT,
                _tokenize.INDENT,
                _tokenize.DEDENT,
                _tokenize.ENDMARKER,
        ):
            continue

        if token.type == _tokenize.ERRORTOKEN:
            raise ErrorToken

        yield token


def parse(tokens: _typing.Iterable[_TokenInfo]):
    tokens = filter_tokens(tokens)
    scope = _Scope()
    scope.push(tokens)

    try:
        next(tokens)
    except StopIteration:
        pass
    else:
        raise Unfinished

    return scope.value


def parse_cmd(args=None):  # pragma: no cover
    import sys
    import argparse
    import json
    from tokenize import tokenize
    from clausewitz.util.tokenize import prepare

    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('--pretty', action='store_true')
    args = parser.parse_args(args)

    with open(args.input, 'rb') as f:
        readline = prepare(f.readline)
        tokens = tokenize(readline)
        value = parse(tokens)

    if args.pretty:
        kwargs = {
            'indent': 4,
        }
    else:
        kwargs = {
            'separators': (',', ':'),
        }

    json.dump(value, sys.stdout, **kwargs)
