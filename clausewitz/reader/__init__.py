class AbstractReader(object):
    def read(self, c):
        raise NotImplementedError

    def cleanup(self):
        pass

    @property
    def result(self):
        raise NotImplementedError
