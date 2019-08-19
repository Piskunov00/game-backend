import pytest

# target:
from api.business import get_colors


def test_that_get_colors_correct_import_json():
    assert type(get_colors(5)) == int
