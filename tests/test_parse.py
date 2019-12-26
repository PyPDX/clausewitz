from tokenize import tokenize

from clausewitz.parse import parse
from clausewitz.tokenize import prepare


def test_parse(sample):
    expected = {
        'a': ['x.000', 'y', 'z'],
        'b': 0,
        'c': 'true',
        'd': -2.1,
        'e.xyz': 'hello\nworl"d',
        'f': {},
    }

    value = parse(tokenize(prepare(sample)))
    assert value == expected
