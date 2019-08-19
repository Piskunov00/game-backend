import pytest
import json
from api.views import *
from api.models import *
from mock import patch
from json import loads
from api.utils.bicycles import cmp
from api.business import get_colors


@pytest.mark.django_db
def test_that_check_view_sign_in(rf):
    request = rf.get('/sign_in/?name=tester&password=p@ssw0rd')
    response = sign_in(request)
    assert response.status_code == 200
    data = json.loads(response.content)
    assert data.pop('token') is not None
    assert data.pop('date_sign_up') is not None  # todo: проверять что ~недавно (сегодня)
    assert data == {
        'result': 1,
        'name': 'tester',
        'password': 'p@ssw0rd',
        'birthday': 'None',
        'sex': 0,
        'money': 228,
        'rating': 0,
        'mileage': 0,
        'hints': True,
    }


@pytest.mark.django_db
def test_that_check_view_sign_up(rf):
    request = rf.post('/sign_up/', data=dict(name='test', password='777'))
    response = sign_up(request)
    assert response.status_code == 201
    new_user = Gamer.objects.get(name='test')
    assert 'sha256$' in new_user.password


@pytest.mark.django_db
def test_that_check_if_login_already_exist(rf):
    request = rf.post('/sign_up/', data=dict(name='tester', password='777'))
    response = sign_up(request)
    assert response.status_code == 400
    assert response.reason_phrase == 'Login already exists'


@pytest.mark.django_db
def test_that_check_sign_up_with_birthday(rf):
    request = rf.post(
        '/sign_up/',
        data=dict(
            name='test',
            password='777',
        )
    )
    response = sign_up(request)
    assert response.status_code == 201
    assert response.reason_phrase == 'Created'


@pytest.mark.django_db
def test_create_game(rf, tester):
    import api.business.actions
    with patch('api.business.actions.choice', return_value=5432):
        request = rf.post('/create_game/', data=dict(type=1))
        request.user = tester

        response = create_game(request)
        assert response.status_code == 201

        json_answer = loads(response.content)
        assert response.reason_phrase == 'Created'
        assert json_answer['result'] == 5432


@pytest.mark.django_db
def test_that_check_that_205_if_there_are_many_games(rf, tester):
    import api.business.actions
    with patch('api.business.actions.choice', side_effect=IndexError()):
        request = rf.post('/create_game/', data=dict(type=1))
        request.user = tester

        response = create_game(request)
        assert response.status_code == 205


@pytest.mark.django_db
@patch('api.business.actions.choice', return_value=7777)
@patch('api.business.actions.time', return_value=10)
def test_that_check_the_ability_to_play_alone(_, __, rf, tester):
    import api.business.actions
    import api.views.gwbmods

    request = rf.post('/create_game/', data=dict(type=1))
    request.user = tester
    response = create_game(request)
    assert response.status_code == 201
    key = loads(response.content)['result']

    request = rf.post('/init_game/')
    request.user = tester
    response = init_game(request)
    assert response.status_code == 200
    assert key == 7777

    gg = GiG.objects.get(gamer=tester)
    game = gg.game

    assert gg.chief
    assert gg.color == 16515072
    assert gg.gamer.id == tester.id
    assert gg.latitude == -1  # изменяется при update_state
    assert gg.longitude == -1  # -||-
    assert gg.status == GiG.StatusGiGChoices.ACTIVE
    dump = gg.__dict__

    assert game.cnt_gamers == 1
    assert game.duration is None
    assert game.status == game.StatusGameChoices.INITIALIZED
    assert game.type_game == 1

    request = rf.post('/begin_game/', data=dict(duration=155))
    request.user = tester
    response = begin_game(request)
    gg = GiG.objects.get(gamer=tester)
    game = gg.game

    assert cmp(gg.__dict__, dump, exclude=['_state'])
    assert game.StatusGameChoices.STARTED == game.status
    assert game.time_end_game == 165
    assert game.duration == 155


@pytest.mark.django_db
@pytest.mark.skip
def test_that_alone_and_non_superuser_cant_begin_game(rf, slave):
    request = rf.post('/create_game/?type=1')
    request.user = slave

    response = create_game(request)
    assert response.status_code == 403

"""
Сделать:
тест когда человек не один,
тест когда человек один но не админ и не может играть в одиночку
тест когда хватают монетку
тест когда завершают игру
тест когда изменяют радиус и хватают монетку
тест когда изменяют радиус но не хватает денег
тест когда update но игра должна закончиться

тест когда играешь с ботом
тест когда изменяешь поле hints
тест что 200 любая вьюха из tofront
тест на calc_distance и все велосипеды 
"""