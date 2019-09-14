from tmp_name.models import (
    Game,
    Gamer,
    GiG,
    Message,
    Coin,
)

from tmp_name.business.functions import duration_to_game
from typing import Dict
from random import choice
from tmp_name.business.functions import get_colors
from tmp_name.exceptions import HttpRequestException
from django.http import HttpResponseServerError
from time import time
from tmp_name.business.functions import coin_distribution
from tmp_name.utils.geo import calc_distance
from tmp_name.business.functions import is_catch
from utils import Outputter
import logging

StatusGameChoices = Game.StatusGameChoices
StatusGiGChoices = GiG.StatusGiGChoices

logger = logging.getLogger(__name__)
my_lazy = Outputter()


class Action(object):
    @classmethod
    def execute(cls, *args, **kwargs):
        """ override this method """
        raise NotImplementedError

    @staticmethod
    def _create_gig(gamer, game, index, chief=False):
        return GiG(
            gamer=gamer,
            game=game,
            color=get_colors(index),
            chief=chief,
            latitude=-1,
            longitude=-1,
        )


class CreateGame(Action):
    INDEX_COLOR_TO_AUTHOR = 0
    view = 'onlinemode.create_game'

    @classmethod
    def execute(cls, author: Gamer, data: Dict):
        try:
            key = cls._choose_key()
        except IndexError:
            raise HttpRequestException(
                status=205,
                reason='there are too many games',
            )

        try:
            cur_game = cls._create_game(key, author, data['type'])
            cur_game.save()
            cur_gig = cls._create_gig(
                author,
                cur_game,
                cls.INDEX_COLOR_TO_AUTHOR,
                chief=True
            )
            cur_gig.save()
        except Exception as e:
            raise HttpRequestException(
                class_error=HttpResponseServerError,
                reason=str(e),
            )

        return {
            'result': key,
            'description': 'Игра и связь игра-человек успешно созданы',
        }

    @staticmethod
    def _choose_key():
        there_are = list(Game.objects.values_list('link', flat=True))
        return choice([key for key in range(1000, 10000) if key not in there_are])

    @staticmethod
    def _create_game(key, author, type_):
        return Game(
            link=key,
            type_game=type_,
            status=str(StatusGameChoices.CREATED),
            cnt_gamers=1,
        )


class JoinGame(Action):
    @classmethod
    def execute(cls, game: Game, player: Gamer):
        cls._create_gig(
            gamer=player,
            game=game,
            index=game.cnt_gamers
        ).save()

        game.cnt_gamers += 1
        game.save()

        return {'result': game.link}


class InitGame(Action):
    @classmethod
    def execute(cls, game, all_gamers):
        time_ = duration_to_game(game, all_gamers)
        game.status = str(StatusGameChoices.INITIALIZED)
        game.save()
        return {'result': time_}  # возвращаем желательное время игры


class BeginGame(Action):
    @classmethod
    def execute(cls, game, all_gamers, duration):
        game.duration = duration
        game.time_end_game = time() + duration
        game.status = StatusGameChoices.STARTED
        game.save()

        coins = coin_distribution(game, all_gamers)

        for coin in coins:
            coin.save()

        return {'result': 1}


class UpdateGame(Action):
    @classmethod
    def execute(cls, player, game, all_gamers, gg, data):
        cls._increase_mileage(
            game=game,
            player=player,
            latitude=data['latitude'],
            longitude=data['longitude'],
        )

        cls._update_gg(
            gg=gg,
            latitude=data['latitude'],
            longitude=data['longitude'],
        )

        cls._check_tackle(
            game=game,
            gg=gg,
            player=player,
        )

        if game.status >= StatusGameChoices.FINISHED:
            return {
                'stats': {
                    'coins': cls._getting_coins(player, game, gg),  # Полученная сумма
                }
            }
        else:
            def hydrate(dct):
                return {key: val for key, val in dct.items() if val is not None}

            return hydrate({
                'gamers': my_lazy(GiG.objects.filter(game=game)),  # Список игроков
                'link': game.link,  # 4 цифры
                'progress': int(game.is_run),  # 0 или 1
                'author': game.author == player,  # true или false
                'type_game': game.type_game,  # [0, 1, 2]
                'timer': cls._get_timer(game),  # Количество секунд
                'coins': cls._get_coins(game, data['coins']),  # Список монет
                'messages': cls._get_messages(game, data['messages']),  # Список сообщений
            })

    @staticmethod
    def _increase_mileage(game, player, latitude, longitude):
        if game.is_run:
            player.mileage += calc_distance(
                gg.latitude,
                gg.longitude,
                latitude,
                longitude,
            )
            player.save()

    @staticmethod
    def _update_gg(gg, latitude, longitude):
        gg.latitude = latitude
        gg.longitude = longitude
        gg.save()

    @staticmethod
    def _check_tackle(game, gg, player):
        for coin in Coin.objects.filter(game=game, taken=False):
            if is_catch(coin, gg):
                coin.taken = True
                coin.whom = player
                coin.save()

    @staticmethod
    def _getting_coins(player, game, gg):
        if game.type_game == 0:
            getting_coins = Coin.objects.filter(game=game, taken=True).count()
        else:
            a = Coin.objects.filter(game=game, taken=True, whom=player).count()
            b = Coin.objects.filter(game=game).count()
            getting_coins = int(30 * a / b)

        player.money += getting_coins
        player.save()
        gg.delete()
        if not GiG.objects.filter(game=game).count():
            game.delete()
        return getting_coins

    @staticmethod
    def _get_timer(game):
        if game.time_end_game:
            return game.time_end_game - time()

    @staticmethod
    def _get_coins(game, coins):
        cur_cnt_coins = Coin.objects.filter(game=game, taken=False).count()
        if coins != cur_cnt_coins:
            return my_lazy(Coin.objects.filter(game=game, taken=False))

    @staticmethod
    def _get_messages(game, messages):
        cur_cnt_messages = Message.objects.filter(gg__game=game).count()
        if messages != cur_cnt_messages:
            return my_lazy(
                Message
                    .objects
                    .filter(gg__game=game)
                    .order_by('date')
            )[messages:]


class KillRunGame(Action):
    @classmethod
    def execute(cls, game, gg):
        if game.cnt_gamers == 1:
            game.delete()
        else:
            game.cnt_gamers -= 1
            game.save()
            gg.delete()


class SendMessage(Action):
    @classmethod
    def execute(cls, gg, text):
        Message(
            gg=gg,
            text=text,
        ).save()


class CheckGame(Action):
    @classmethod
    def execute(cls, player):
        gg = GiG.objects.filter(gamer=player).count()
        if not gg:
            return {'result': 1}
        game: Game = gg.game

        return {
            'result': 2,
            'link': int(game.link),
            'own': int(game.author == player),
            'run': int(game.started),
        }


class KickPlayer(Action):
    @classmethod
    def execute(cls, target_gg):
        target_gg.delete()  # fixme
