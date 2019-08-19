import pytest
import socket
import time
import os
from django.contrib.auth.hashers import make_password
from api.models import Gamer
from backend.test_settings import DB_HOST, DB_PORT


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
    Gamer(
        name='tester',
        password=make_password('p@ssw0rd'),
        money=228,
        is_superuser=True,
    ).save()
    return Gamer.objects.get(name='tester')


@pytest.fixture(autouse=True)
def slave(db):
    Gamer(
        name='slave',
        password=make_password('slave'),
        money=500,
        is_superuser=False,
    ).save()
    return Gamer.objects.get(name='slave')
