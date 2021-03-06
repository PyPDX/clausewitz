import tokenize

from clausewitz.util.tokenize import prepare


def test_prepare(data):
    expected = b'''\
a = { x.000 """y""" 10z }
b= 0
c =true
d>=-2.1
e.xyz = """hello
worl\\"d\\""""
f = {}
d < 100
# this is a comment
    color = rgb { 100 200 50 }
'''

    with data('sample.txt') as readline:
        readline = prepare(readline)
        for line in expected.splitlines(keepends=True):
            assert readline() == line
        assert readline() == b''


def test_tokenize(data):
    expected = (
        (tokenize.ENCODING, 'utf-8'),

        (tokenize.NAME, 'a'),
        (tokenize.OP, '='),
        (tokenize.OP, '{'),
        (tokenize.NAME, 'x'),
        (tokenize.NUMBER, '.000'),
        (tokenize.STRING, '"""y"""'),
        (tokenize.NUMBER, '10'),
        (tokenize.NAME, 'z'),
        (tokenize.OP, '}'),
        (tokenize.NEWLINE, '\n'),

        (tokenize.NAME, 'b'),
        (tokenize.OP, '='),
        (tokenize.NUMBER, '0'),
        (tokenize.NEWLINE, '\n'),

        (tokenize.NAME, 'c'),
        (tokenize.OP, '='),
        (tokenize.NAME, 'true'),
        (tokenize.NEWLINE, '\n'),

        (tokenize.NAME, 'd'),
        (tokenize.OP, '>='),
        (tokenize.OP, '-'),
        (tokenize.NUMBER, '2.1'),
        (tokenize.NEWLINE, '\n'),

        (tokenize.NAME, 'e'),
        (tokenize.OP, '.'),
        (tokenize.NAME, 'xyz'),
        (tokenize.OP, '='),
        (tokenize.STRING, '"""hello\nworl\\"d\\""""'),
        (tokenize.NEWLINE, '\n'),

        (tokenize.NAME, 'f'),
        (tokenize.OP, '='),
        (tokenize.OP, '{'),
        (tokenize.OP, '}'),
        (tokenize.NEWLINE, '\n'),

        (tokenize.NAME, 'd'),
        (tokenize.OP, '<'),
        (tokenize.NUMBER, '100'),
        (tokenize.NEWLINE, '\n'),

        (tokenize.COMMENT, '# this is a comment'),
        (tokenize.NL, '\n'),

        (tokenize.INDENT, '    '),
        (tokenize.NAME, 'color'),
        (tokenize.OP, '='),
        (tokenize.NAME, 'rgb'),
        (tokenize.OP, '{'),
        (tokenize.NUMBER, '100'),
        (tokenize.NUMBER, '200'),
        (tokenize.NUMBER, '50'),
        (tokenize.OP, '}'),
        (tokenize.NEWLINE, '\n'),
        (tokenize.DEDENT, ''),

        (tokenize.ENDMARKER, ''),
    )

    with data('sample.txt') as readline:
        tokens = tokenize.tokenize(prepare(readline))
        for val in expected:
            token = next(tokens)
            assert (token.type, token.string) == val

        assert tuple(tokens) == ()
