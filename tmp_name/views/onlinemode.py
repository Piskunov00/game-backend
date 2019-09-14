from tmp_name.forms import *

from tmp_name.business import actions
from tmp_name.business import validators
from django.http import JsonResponse

from tmp_name.utils.http_ import Stage, check_request
from django.http import HttpResponse
from utils import MagicOrder

from tmp_name.exceptions import HttpRequestException
import logging

logger = logging.getLogger(__name__)


def create_game(request):
    try:
        data = check_request(
            request=request,
            class_form=CreateGameForm,
            stage=Stage.FULL,
            method='POST',
        )
        author = request.user

        return JsonResponse(
            actions.CreateGame.execute(
                author=author,
                data=data,
            ),
            status=201,
        )
    except HttpRequestException as e:
        return e.response


def join_game(request):
    try:
        data = check_request(
            request=request,
            class_form=JoinGameForm,
            stage=Stage.FULL,
            method='POST',
        )
        player = request.user

        game = MagicOrder('\
        game')(
            validators.JoinGame.validate(data)
        )

        return JsonResponse(
            actions.JoinGame.execute(
                game=game,
                player=player,
            ),
            status=200,
        )
    except HttpRequestException as e:
        return e.response


def init_game(request):
    try:
        check_request(
            request=request,
            stage=Stage.ONLY_AUTHENTICATING,
            method='POST',
        )
        player = request.user

        game, all_gamers = MagicOrder('\
        game, all_gamers')(
            validators.SyncGame.validate(player)
        )

        return JsonResponse(
            actions.InitGame.execute(
                game=game,
                all_gamers=all_gamers,
            ),
            status=200,
        )

    except HttpRequestException as e:
        return e.response


def begin_game(request):
    try:
        data = check_request(
            request=request,
            class_form=BeginGameForm,
            stage=Stage.FULL,
            method='POST',
        )
        player = request.user

        game, all_gamers = MagicOrder('\
        game, all_gamers')(
            validators.BeginGame.validate(
                player=player,
            )
        )

        actions.BeginGame.execute(
            game=game,
            all_gamers=all_gamers,
            duration=data['duration'],
        )
        return HttpResponse(
            status=200,
        )
    except HttpRequestException as e:
        return e.response


def update_state_game(request):
    try:
        data = check_request(
            request=request,
            class_form=UpdateStateForm,
            stage=Stage.FULL,
        )
        player = request.user

        game, all_gamers, gg = MagicOrder('\
        game, all_gamers, gg')(
            validators.GiGDetail.validate(player)
        )

        retval = actions.UpdateGame.execute(
            player=player,
            game=game,
            all_gamers=all_gamers,
            gg=gg,
            data=data,
        )
        return JsonResponse(
            data=retval,
            status=200,
        )

    except HttpRequestException as e:
        return e.response


def kill_run_game(request):
    try:
        check_request(
            request=request,
            stage=Stage.ONLY_AUTHENTICATING,
        )
        player = request.user

        game, gg = MagicOrder('\
        game, gg')(
            validators.GiGDetail.validate(player)
        )

        actions.KillRunGame.execute(
            game=game,
            gg=gg,
        )
        return HttpResponse(
            status=200,
        )
    except HttpRequestException as e:
        return e.response


def send_message(request):
    try:
        data = check_request(
            request=request,
            class_form=SendMessageForm,
            stage=Stage.FULL,
            method='POST',
        )
        player = request.user

        gg = MagicOrder('\
        gg')(
            validators.GiGDetail.validate(player)
        )

        actions.SendMessage.execute(
            gg, data['text'],
        )
        return HttpResponse(
            reason='Created',
            status=201,
        )
    except HttpRequestException as e:
        return e.response


def check_game(request):
    try:
        check_request(
            request=request,
            stage=Stage.ONLY_AUTHENTICATING,
        )
        player = request.user

        return JsonResponse(
            actions.CheckGame.execute(player),
            status=200,
        )
    except HttpRequestException as e:
        return e.response


def kick_player(request):
    try:
        data = check_request(
            request=request,
            class_form=KickPlayerForm,
            stage=Stage.FULL,
            method='POST',
        )
        player = request.user

        target = MagicOrder('\
        target')(
            validators.KickPlayer.validate(
                player,
                data['target'],
            )
        )

        actions.KickPlayer.execute(target)
        return JsonResponse(
            {'result': 1}
        )
    except HttpRequestException as e:
        return e.response


def change_radius(request):
    try:
        data = check_request(
            request=request,
            class_form=ChangeRadiusForm,
            stage=Stage.FULL,
            method='POST',
        )
        user = request.user

        cost, gg = MagicOrder('\
        cost, gg')(
            validators.ChangeRadius.validate(user, data)
        )
        user.money -= data['cost']
        gg.radius = data['radius']
        user.save()
        gg.save()
        return JsonResponse(
            {'result': user.money},
            status=200,
        )
    except HttpRequestException as e:
        return e.response