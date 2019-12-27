from tokenize import tokenize

import pytest

from clausewitz.parse import parse, Unfinished
from clausewitz.tokenize import prepare


def test_parse(data):
    expected = {
        '__dupkeys__': {
            'd': ['d', 'd+1'],
        },
        '__ops__': {
            'd': '>=',
            'd+1': '<',
        },
        'a': ['x.000', 'y', '10z'],
        'b': 0,
        'c': 'true',
        'd': -2.1,
        'e.xyz': 'hello\nworl"d"',
        'f': {},
        'd+1': 100,
    }

    with data('sample.txt') as readline:
        value = parse(tokenize(prepare(readline)))
    assert value == expected


def test_parse_unfinished(data):
    with data('error-unfinished.txt') as readline:
        with pytest.raises(Unfinished):
            parse(tokenize(prepare(readline)))
