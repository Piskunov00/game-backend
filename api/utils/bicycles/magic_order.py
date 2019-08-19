class MagicOrder(object):
    def __init__(self, order=None):
        self._order = (order or '') \
            .replace('\n', '') \
            .replace(' ', '') \
            .split(',')

    def __call__(self, dct=None, **kwargs):
        kwargs.update(dct or {})
        return [kwargs.get(key) for key in self._order]