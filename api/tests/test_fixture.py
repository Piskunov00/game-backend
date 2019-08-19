import pytest
from django.contrib.auth.hashers import make_password
from api.models import Gamer


@pytest.mark.django_db
def test_that_there_is_tester_in_database():
    tester = Gamer.objects.get(name='tester')
    assert tester.name == 'tester'
    assert tester.money == 228
