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
from api.models import Gamer
from api.exceptions import HttpRequestException
from api.utils.bicycles import Stage

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
        token = dict(request.headers).get('Token')
        if token:
            request.user = auth_with_token(token)
        elif not request.user.is_authenticated:
            raise HttpRequestException(
                class_error=HttpResponse,
                reason='Unauthorized',
                status=401,
            )

    return retval


def auth_with_token(token):
    try:
        payload = jwt_decode_handler(token)
        username = jwt_get_username_from_payload(payload)
        return Gamer.objects.get(name=username)
    except ObjectDoesNotExist:
        raise HttpRequestException(
            class_error=Http404,
            reason='User does not exist',
        )
    except MultipleObjectsReturned:
        raise HttpRequestException(
            class_error=HttpResponseServerError,
            reason='In the problem database: there were two identical logins',
        )
    except Exception as e:
        if str(e) == 'Signature has expired':
            response = HttpResponseRedirect(
                redirect_to=reverse('api:sign_in'),
                reason='Token is out of date, go through authorization again',
            )
            raise HttpRequestException(
                ready_response=response,
            )
        raise HttpRequestException(
            class_error=HttpResponseForbidden,
            reason='Invalid Token',
        )
