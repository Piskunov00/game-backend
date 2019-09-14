from math import sin, cos, sqrt, atan2, radians


def calc_distance(lat1, lon1, lat2, lon2) -> float:
    """ Params may be is instance of string """
    R = 6373.0

    lat1 = radians(abs(float(lat1)))
    lon1 = radians(abs(float(lon1)))
    lat2 = radians(abs(float(lat2)))
    lon2 = radians(abs(float(lon2)))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c * 1000
