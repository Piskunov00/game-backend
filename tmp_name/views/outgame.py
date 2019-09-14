from django.shortcuts import render
from django.http import HttpResponseServerError
from django.http import HttpResponse

from tmp_name.utils.base import http_wrapper, get_user
from tmp_name.models import Gamer
from utils.auth import authenticate, login

from re import search
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt


def show_users(request):
    lst = Gamer.objects.all()
    return render(request, "users.html", {"users": lst})


def sign_in(request):
    get = request.GET

    if not all(map(lambda a: a in get, ['name', 'password'])):
        return HttpResponse(
            status=400,
            reason='name and password required',
        )

    player = authenticate(
        username=get['name'],
        password=get['password'],
        app='tmp_name'
    )

    if player is None:
        return HttpResponse(
            status=401,
            reason='Authentication failed',
        )

    if hasattr(request, 'session'):
        login(request, player)

    token = player.get_token()

    return http_wrapper(
        {
            'result': 1,
            'name': player.username,
            'password': get['password'],
            'birthday': str(player.birthday),
            'date_sign_up': str(player.date_sign_up),
            'sex': player.sex,
            'money': player.money,
            'rating': player.rating,
            'mileage': player.mileage,
            'hints': player.hints,
            'token': token,
        }
    )


@csrf_exempt
def sign_up(request):
    data = request.POST
    if Gamer.objects.filter(user__username=data['name']).count():
        return HttpResponse(
            reason='Login already exists',
            status=400,
        )
    birthday = data.get('birthday', None)
    if birthday:
        birthday = datetime.strptime(birthday, "%d-%m-%Y")
    sex = data.get('sex', 0)

    Gamer.create_new(
        username=data['name'],
        password=data['password'],
        sex=sex,
        birthday=birthday,
        mileage=0,
        money=0,
        rating=0,
        hints=True,
    )

    player = authenticate(
        username=data['name'],
        password=data['password'],
        app='tmp_name'
    )
    if not player:
        return HttpResponseServerError()
    if hasattr(request, 'session'):
        login(request, player)
    return http_wrapper({'result': 1}, status=201)


def change_coins(request):
    get = request.GET
    player = get_user(get['name'])
    if player.money + int(get['count']) < 0:
        return http_wrapper({'result': -1})
    player.money += int(get['count'])
    player.save()
    return http_wrapper({'result': player.money})


def change_rating(request):
    get = request.GET
    player = get_user(get['name'])
    if player.rating + int(get['count']) < 0:
        return http_wrapper({'result': -1})
    player.rating += int(get['count'])
    player.save()
    return http_wrapper({'result': player.rating})


def check(search_, reg, name):
    if name == "":
        return True
    if reg:
        if search(search_, name) is None:
            return False
        else:
            return True
    else:
        if search_ in name:
            return True
        else:
            return False


def get_top_users(request):
    # search, reg
    get = request.GET
    reg = bool(get['reg'])
    search_ = get['search']
    return http_wrapper([
        {
            'name': gamer.name,
            'rating': gamer.rating,
            'mileage': gamer.mileage,
        }
        for gamer in Gamer.objects.all()
        if check(search_, reg, gamer.name)
    ][:50])


def change_show_hints(request):
    get = request.GET
    user = get_user(get['name'])
    user.hints = (get['value'] == 'true')
    user.save()
    return http_wrapper({'result': 1})
