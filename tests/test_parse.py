from tokenize import tokenize

from clausewitz.parse import parse
from clausewitz.tokenize import prepare


def test_parse(sample):
    expected = {
        'a': ['x.000', 'y'],
        'b': 0,
        'c': 1,
        'd': -2.1,
        'e.xyz': 'hello\nworl"d',
    }

    value = parse(tokenize(prepare(sample)))
    assert value == expected
