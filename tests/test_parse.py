from tokenize import tokenize

from clausewitz.parse import parse
from clausewitz.tokenize import prepare


def test_parse(sample):
    expected = {
        '__dupkeys__': {
            'd': ['d', 'd+1'],
        },
        'a': ['x.000', 'y', '10z'],
        'b': 0,
        'c': 'true',
        'd': -2.1,
        'e.xyz': 'hello\nworl"d"',
        'f': {},
        'd+1': 100,
    }

    value = parse(tokenize(prepare(sample)))
    assert value == expected
