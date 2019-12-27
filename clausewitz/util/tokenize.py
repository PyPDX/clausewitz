def prepare(readline):
    """
    Prepare for Python's `tokenize`.
    Replace quotes with triple quotes to support multiline strings.
    """

    def _readline():
        line = readline()
        # don't replace \", only "
        return line.replace(
            rb'\"', b"'''''",  # Pretend that there will never be ''''' in the text
        ).replace(
            b'"', b'"""',
        ).replace(
            b"'''''", rb'\"',
        )

    return _readline


def prepare_cmd(args=None):  # pragma: no cover
    import sys
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filename', nargs='?',
    )
    args = parser.parse_args(args)

    f = None

    try:
        if args.filename is None:
            # use stdout
            readline = sys.stdin.buffer.readline
        else:
            f = open(args.filename, 'rb')
            readline = f.readline

        readline = prepare(readline)

        while True:
            line = readline()
            if not line:
                break
            sys.stdout.buffer.write(line)
            sys.stdout.buffer.flush()

    finally:
        if f is not None:
            f.close()
