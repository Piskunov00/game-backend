import pytest
import socket
import time
import os
from django.contrib.auth.hashers import make_password
from backend.test_settings import DB_HOST, DB_PORT

from tmp_name.models import Gamer
from utils.models import User


@pytest.fixture(autouse=True, scope='session')
def a_wait_for_psql():
    max_attempts = 100

    for _ in range(max_attempts):
        try:
            sock = socket.socket()
            sock.connect((DB_HOST, DB_PORT))
            sock.close()
            return
        except Exception:
            time.sleep(0.5)
            pass

    raise IOError('Cant connect to database')


@pytest.fixture(autouse=True)
def tester(db):
    """ Created tester :: Gamer """
    user = User.objects.get_or_create(
        username='tester',
        password=make_password('p@ssw0rd'),
        is_superuser=True,
    )[0]
    Gamer.objects.get_or_create(
        user=user,
        money=228,
    )
    return Gamer.objects.get(user__username='tester')


@pytest.fixture(autouse=True)
def slave(db):
    user = User.objects.get_or_create(
        username='slave',
        password=make_password('slave'),
        is_superuser=False,
    )[0]
    Gamer.objects.get_or_create(
        user=user,
        money=500,
    )
    return Gamer.objects.get(user__username='slave')
