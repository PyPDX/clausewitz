import typing as _typing


class Dict(dict):
    DUPKEYS = '__dupkeys__'
    OPS = '__ops__'

    def __init__(self, iterable=()):
        super().__init__()
        for k, v in iterable:
            self[k] = v

    def _get_meta(self, key):
        if key not in self:
            super().__setitem__(key, {})
        return self[key]

    @property
    def dupkeys(self) -> _typing.Dict[str, _typing.List[str]]:
        return self._get_meta(self.DUPKEYS)

    @property
    def ops(self) -> _typing.Dict[str, str]:
        return self._get_meta(self.OPS)

    def __setitem__(self, key, value):
        op, v = value

        if key in self:
            if key not in self.dupkeys:
                self.dupkeys[key] = [key]
            new_key = f'{key}+{len(self.dupkeys[key])}'
            self.dupkeys[key].append(new_key)
            key = new_key

        if op != '=':
            self.ops[key] = op

        return super().__setitem__(key, v)
