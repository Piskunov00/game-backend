import pytest
from api.utils.bicycles import *


def test_magic_order():
    data = dict(
        a=1,
        b=2,
        c=3,
        d=4,
        e=5,
        f=6,
    )

    a, b, c, d, e, f = MagicOrder('\
    a, b, c, d, e, f')(data)

    assert [a, b, c, d, e, f] == [1, 2, 3, 4, 5, 6]

    data = dict(
        f=1,
        e=4,
        a=5,
        d=2,
        c=3,
        b=6,
    )

    a, b, c, d, e, f = MagicOrder('\
    a, b, c, d, e, f')(data)

    assert [a, b, c, d, e, f] == [5, 6, 3, 2, 4, 1]
