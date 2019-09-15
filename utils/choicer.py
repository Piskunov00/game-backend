def choicer(origin):
    """ todo: описание
    _order по возрастанию
    """
    class Item:
        def __init__(self, key, value, weight=0):
            self._key = key
            self._value = value
            self._weight = weight

        def view(self):
            return (self._value, self._key)

        def __gt__(self, other):
            if not hasattr(other, '_weight'):
                raise NotImplementedError
            return self._weight > other._weight

        def __ge__(self, other):
            if not hasattr(other, '_weight'):
                raise NotImplementedError
            return self._weight >= other._weight

        def __str__(self):
            return str(self._value)

        def __eq__(self, other):
            return str(self._value) == str(other)

    def as_list(cls):
        return [
            item.view() for item in cls._items
        ]

    def convert(cls, value):
        return cls._map_[value]

    origin.as_list = classmethod(as_list)
    origin.convert = classmethod(convert)
    origin._items = []
    origin._map_ = dict()
    for number, (key, value) in enumerate(origin.__dict__.items()):
        if key.startswith('_') or type(value) != str:
            continue
        if not hasattr(origin, '_order'):
            mind = Item(key, value)
        else:
            mind = Item(key, value, origin._order.index(value))
        origin._items.append(mind)
        origin._map_[value] = mind
        setattr(origin, key, mind)
    return origin
