from django.contrib.staticfiles import finders

from typing import List
from math import ceil
from random import gauss
from json import load

from tmp_name.utils.geo import calc_distance

from tmp_name.models import (
    Game,
    Coin,
    GiG,
)


def coin_distribution(game: Game, ggs: List[GiG]):
    # todo: что-то сделать с этом функцией чтобы не было так страшно
    min_latitude = min(filter(None, [gg.latitude for gg in ggs]))
    min_longitude = min(filter(None, [gg.longitude for gg in ggs]))
    max_latitude = max(filter(None, [gg.latitude for gg in ggs]))
    max_longitude = max(filter(None, [gg.longitude for gg in ggs]))

    speed = 4 * 1000 / 3600

    med_latitude = sum(filter(None, [gg.latitude for gg in ggs])) / len(ggs)
    med_longitude = sum(filter(None, [gg.longitude for gg in ggs])) / len(ggs)

    p0_0 = ggs[0].latitude
    p0_1 = ggs[0].longitude
    p1_0 = ggs[0].latitude + 0.05
    p1_1 = ggs[0].longitude

    in_005_deg_m = calc_distance(p0_0, p0_1, p1_0, p1_1)
    num_ggs = len(ggs)
    if num_ggs == 1:
        num_ggs += 1
    sigma = speed * game.duration * (num_ggs / (num_ggs - 1)) * 2 / 10 * 0.05 / in_005_deg_m

    coins_num = 5 * num_ggs
    if game.duration > 600:
        coins_num += int((game.duration // 60 - 10) * 0.1 * num_ggs)

    min_interval = sigma / 6 / 0.05 * in_005_deg_m

    coins_loc = [[gauss(med_latitude, sigma), gauss(med_longitude, sigma)]]
    while len(coins_loc) < coins_num:
        t = 1
        latitude = gauss(med_latitude, sigma)
        longitude = gauss(med_longitude, sigma)
        for j in coins_loc:
            if calc_distance(j[0], j[1], latitude, longitude) < min_interval:
                t = 0
        if t:
            coins_loc.append([latitude, longitude])

    min_latitude -= 0.005
    max_latitude += 0.005
    min_longitude -= 0.005
    max_longitude += 0.005

    return [
        Coin(
            latitude=i[0],
            longitude=i[1],
            game=game,
            cost=1,
            taken=False,
            size=15,
        ) for i in coins_loc
    ]


def duration_to_game(game: Game, ggs: List[GiG]):
    speed = 6 * 1000 / 3600

    med_latitude = sum(filter(None, [gg.latitude for gg in ggs])) / len(ggs)
    med_longitude = sum(filter(None, [gg.longitude for gg in ggs])) / len(ggs)

    some_dist = calc_distance(
        med_latitude,
        med_longitude,
        ggs[0].latitude,
        ggs[0].longitude,
    )

    return ceil(some_dist / speed)


def is_catch(coin: Coin, gg: GiG) -> bool:
    return calc_distance(
        coin.latitude,
        coin.longitude,
        gg.latitude,
        gg.longitude,
    ) <= coin.size + gg.radius


def get_colors(ind: int) -> int:
    return int(load(open((finders.find('get_colors.json'))))['colors'][ind], 16)
