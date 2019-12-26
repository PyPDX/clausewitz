import typing as _typing


class DupKeyDict(dict):
    KEY = '__dupkeys__'

    def __init__(self, iterable=()):
        super().__init__()
        for k, v in iterable:
            self[k] = v

    @property
    def dupkeys(self) -> _typing.Dict[str, _typing.List[str]]:
        if self.KEY not in self:
            super().__setitem__(self.KEY, {})
        return self[self.KEY]

    def __setitem__(self, key, value):
        if key in self:
            if key not in self.dupkeys:
                self.dupkeys[key] = [key]
            new_key = f'{key}+{len(self.dupkeys[key])}'
            self.dupkeys[key].append(new_key)
            return super().__setitem__(new_key, value)

        return super().__setitem__(key, value)
