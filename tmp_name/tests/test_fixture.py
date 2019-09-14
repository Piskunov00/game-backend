import pytest
from django.contrib.auth.hashers import make_password
from tmp_name.models import Gamer


@pytest.mark.django_db
def test_that_there_is_tester_in_database():
    tester = Gamer.objects.get(user__username='tester')
    assert tester.user.username == 'tester'
    assert tester.money == 228
