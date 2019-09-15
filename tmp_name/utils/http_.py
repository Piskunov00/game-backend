from enum import Enum

from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseServerError,
    HttpResponseRedirect,
    Http404,
)

from django.http import HttpRequest
from rest_framework_jwt.authentication import (
    jwt_get_username_from_payload,
    api_settings,
)
from django.urls import reverse
from django.core.exceptions import (
    ObjectDoesNotExist,
    MultipleObjectsReturned,
)
from tmp_name.models import Gamer
from tmp_name.exceptions import HttpRequestException
from utils import Stage

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


def check_request(request, class_form=None, method='GET', stage=Stage.FULL):
    retval = None

    if stage['validate_form'] and class_form:
        form = class_form(request.__getattribute__(method))
        if not form.is_valid():
            raise HttpRequestException(
                class_error=HttpResponseBadRequest,
                reason=form.errors,
            )
        retval = form.cleaned_data

    if stage['authenticated']:
        if not request.user.is_authenticated:
            raise HttpRequestException(
                class_error=HttpResponse,
                reason='Unauthorized',
                status=401,
            )
        request.user = Gamer.objects.get(user=request.user)

    return retval
