from tmp_name.models import (
    Game,
    Gamer,
    GiG,
)

from typing import List

from django.core.exceptions import (
    ObjectDoesNotExist,
)

from django.http import (
    HttpResponseForbidden,
    HttpResponseNotFound,
)
from functools import reduce
from django.db.models import Q

from tmp_name.exceptions import HttpRequestException

from tmp_name.models import StatusGameChoices, StatusGiGChoices


class Validator(object):

    def validate(self, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def get_games_with_string_invite(string_invite):
        """ Общий метод получения игры по инвайту """
        try:
            return Game.objects.get(link=string_invite)
        except ObjectDoesNotExist:
            raise HttpRequestException(
                reason='Игра с такой string_invite не найдена',
                class_error=HttpResponseNotFound,
            )


class JoinGame(Validator):
    @classmethod
    def validate(cls, data):
        return dict(
            game=cls._get_game(data['string_invite']),
        )

    @classmethod
    def _get_game(cls, string_invite):
        game = cls.get_games_with_string_invite(string_invite)

        if game.is_block:
            raise HttpRequestException(
                reason='You are not allowed to enter this game',
                class_error=HttpResponseForbidden,
            )
        return game


class SyncGame(Validator):
    @classmethod
    def validate(cls, player: Gamer):
        game = cls.game(player)
        all_gamers = cls.all_gamers(game)
        gig = GiG.objects.get(game=game, gamer=player)

        if not gig.chief:
            raise HttpRequestException(
                class_error=HttpResponseForbidden,
                reason='You are not the creator of the game',
            )

        if game.cnt_gamers == 1 and not player.user.is_superuser:
            raise HttpRequestException(
                status=205,
                reason='You can\'t start playing alone',
            )

        return dict(
            game=game,
            all_gamers=all_gamers,
        )

    @staticmethod
    def game(player: Gamer) -> Game:
        try:
            active = reduce(lambda q, v: q | v, [
                Q(status=Game.StatusGameChoices.CREATED),
                Q(status=Game.StatusGameChoices.INITIALIZED),
                Q(status=Game.StatusGameChoices.CREATED),
            ], Q())
            return Game.objects.get(
                active,
                players__in=[player],
            )
        except ObjectDoesNotExist:
            raise HttpRequestException(
                class_error=HttpResponseNotFound,
                reason='No current games',
            )

    @staticmethod
    def all_gamers(game: Game) -> List[Gamer]:
        return GiG.objects.filter(game=game)


class BeginGame(SyncGame):
    @classmethod
    def validate(cls, player: Gamer):
        game, all_gamers = super().validate(player).values()

        if StatusGameChoices.convert(game.status) > StatusGameChoices.INITIALIZED:
            raise HttpRequestException(
                class_error=HttpResponseForbidden,
                reason='Game already started',
            )

        return dict(
            game=game,
            all_gamers=all_gamers,
        )


class GiGDetail(SyncGame):
    @classmethod
    def validate(cls, player: Gamer):
        game = cls.game(player)
        all_gamers = cls.all_gamers(game)
        gg = GiG.objects.get(gamer=player, game=game)
        return dict(
            game=game,
            all_gamers=all_gamers,
            gg=gg,
        )


class KickPlayer(Validator):
    @classmethod
    def validate(cls, from_user, player_name):
        try:
            player = Gamer.objects.get(player_name)
            return dict(
                target=GiG.objects.get(gamer=player)
            )
        except ObjectDoesNotExist:
            raise HttpRequestException(
                class_error=HttpResponseNotFound,
                reason='There are no such people',
            )


class ChangeRadius(Validator):
    @classmethod
    def validate(cls, user, data):
        if user.money < data['cost']:
            raise HttpRequestException(
                status=205,
                reason='Insufficient funds',
            )
        try:
            gg = GiG.objects.get(gamer=user)
        except ObjectDoesNotExist:
            raise HttpRequestException(
                class_error=HttpResponseNotFound,
                reason='No communication game player',
            )
        return dict(
            cost=data['cost'],
            gg=gg,
        )
