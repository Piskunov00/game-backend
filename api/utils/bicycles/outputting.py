from enum import Enum
from django.forms.models import model_to_dict as django_model_to_dict
from backend.settings import OUTPUTTER_PARAMS
from django.db.models.query import QuerySet
from functools import reduce


class Like(Enum):
    WITH_BUSINESS_LOGIC = 'BUSINESS'
    IN_PARAMS = 'PARAMS'


def memories(func):
    """ Положить в аттрибут первого аргумета второй """
    def wraps(*args, **kwargs):
        args[0].__setattr__('memories', args[1])
        return func(*args, **kwargs)
    return wraps


def model_to_dict(instance, fields=None, exclude=None, upgrade=True):
    """
    Это расширение для :django.forms.models.model_to_dict: данная
     функция в fields может принимать список из строк и кортежей,
     где кортежи определяют как назвать в итоговом словаре поле и путь до него
    А можно указать upgrade=False и воспользоваться джанговской реализацией
    """
    if not upgrade:
        return django_model_to_dict(instance, fields, exclude)
    data = {}
    fields = {
        key: value for key, value in map(
            lambda x: x if isinstance(x, tuple) else (x, x),
            fields
        )
    }
    for name, path in fields:
        data[name] = reduce(
            lambda obj, attr: obj.__getattribute__(attr),
            path.split('.'),
            instance,
        )
    return data


class Outputter(object):
    @memories
    def __call__(self, list_or_instance, fields=None, like=Like.WITH_BUSINESS_LOGIC):

        list_with_models, behavior = {
            True: (list_or_instance, lambda l: l),
            False: ([list_or_instance], lambda l: l[0]),
        }[self._is_list]

        if like == Like.WITH_BUSINESS_LOGIC:
            bus_fields = OUTPUTTER_PARAMS.get(f'{self._get_class(behavior(list_with_models))}', [])
            fields = bus_fields.extends(fields or [])

        if not fields:
            fields = None

        return behavior([
            model_to_dict(model, fields)
            for model in list_with_models
        ])

    @property
    def _is_list(self):
        return isinstance(
            self.__getattribute__('memories'),
            (tuple, list, QuerySet)
        )

    @staticmethod
    def _get_class(o):
        return str(o.__class__).split('.')[-1]
