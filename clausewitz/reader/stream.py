class Stream(object):
    def __init__(self, iterable):
        if isinstance(iterable, Stream):
            self.__iter = iterable.__iter
        else:
            self.__iter = iter(iterable)

    def __iter__(self):
        return self.__iter


class FileStream(Stream):
    def __init__(self, f_or_fname):
        self.__f = None

        if isinstance(f_or_fname, str):
            self.__f = open(f_or_fname)
            super().__init__(self.file_iter(self.__f))

        else:
            super().__init__(self.file_iter(f_or_fname))

    def file_iter(self, f):
        try:
            for line in f:
                for c in line:
                    yield c
        finally:
            if self.__f is not None:
                self.__f.close()

    @property
    def closed(self):
        return self.__f.closed
