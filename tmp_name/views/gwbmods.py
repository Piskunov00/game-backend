# import from my files
from tmp_name.utils.geo import calc_distance

from tmp_name.forms import *
from tmp_name.models import BotGame, Gamer
from django.views.decorators.csrf import csrf_exempt
from django.http import (
    JsonResponse,
    HttpResponse,
    HttpResponseNotFound,
)
from django.views.decorators.http import (
    require_POST,
    require_GET,
)

from time import time


@csrf_exempt
@require_POST
def kill_gwb(request):
    game = BotGame.objects.filter(gamer=request.user).first()
    if not game:
        return HttpResponseNotFound(
            reason='Game not found'
        )
    game.delete()
    return HttpResponse('Ok')


@csrf_exempt
@require_POST
def update_gwb(request):
    form = UpdateGameWithBot(request.POST)
    if form.is_valid():
        data = form.cleaned_data

        game: BotGame = BotGame.objects.filter(gamer=request.user).first()
        if not game:
            return HttpResponseNotFound(
                reason='Game not found'
            )

        if data['update_dist']:
            game.path += calc_distance(
                data['latitude'],
                data['longitude'],
                game.user_latit,
                game.user_long
            )
        game.user_latit = data['latitude']
        game.user_long = data['longitude']

        return HttpResponse('Ok')
    else:
        return HttpResponse(
            status=400,
            reason=form.errors,
        )


@require_POST
def stop_in_gwb(request):
    game: BotGame = BotGame.objects.filter(gamer=request.user).first()
    if game is None:
        return HttpResponseNotFound(reason='Game not found')
    game.cnt_stops += 1
    game.save()
    return HttpResponse('Ok')


@require_GET
def gwb_detail(request):
    user = request.user
    game: BotGame = BotGame.objects.filter(gamer=user).first()

    if not game:
        return HttpResponseNotFound(
            reason='Game not found'
        )

    return JsonResponse({
        'result': 1,
        'alpha': game.alpha,
        'speed': game.speed,
        'time': int(time() - game.date),
        'begin_latit': game.begin_latit,
        'begin_long': game.begin_long,
        'end_latit': game.end_latit,
        'end_long': game.end_long,
        'stops': game.cnt_stops,
    })


@require_GET
def get_my_speed_gwb(request):
    user = request.user
    game = BotGame.objects.filter(gamer=user).first()
    secs = time() - game.date
    return JsonResponse(
        {'result': game.path / secs}
    )


@csrf_exempt
@require_POST
def create_gwb(request):
    request.user = Gamer.objects.get(name='ifrag')
    form = CreateGameWithBot(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        BotGame.objects.filter(gamer=request.user).delete()
        BotGame(
            gamer=request.user,
            alpha=data['alpha'],
            speed=data['speed'],
            path=0,
            date=time(),
            begin_latit=data['begin_latit'],
            begin_long=data['begin_long'],
            end_latit=data['end_latit'],
            end_long=data['end_long'],
            cnt_stops=0,
        ).save()
        return JsonResponse({'result': 1})
    else:
        return HttpResponse(
            status=400,
            reason=form.errors,
        )
