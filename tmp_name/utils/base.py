from django.http import HttpResponse

from tmp_name.models import Gamer

import json
import logging

logger = logging.getLogger(__name__)


def http_wrapper(obj, status=200):
    logger.warning('использование устаревшей функции http_wrapper')
    return HttpResponse(json.dumps(obj), status=status)


def get_user(name: str) -> Gamer:
    logger.warning('Использование устаревшей функции get_user')
    return Gamer.objects.get(name=name)
