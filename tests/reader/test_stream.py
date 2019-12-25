from clausewitz.reader.stream import Stream, FileStream

s = 'jafieoea'
s2 = '''
hua3ion
gi4qpndm
'''


def test_string_stream():
    assert list(Stream(s)) == list(s)
    assert list(Stream(s2)) == list(s2)


def test_file_stream(tmpdir):
    d = tmpdir / 'reader'
    d.mkdir()
    f = d / 'f.txt'
    f.write(s2)
    fs = FileStream(str(f))
    assert list(fs) == list(s2)
    assert fs.closed
