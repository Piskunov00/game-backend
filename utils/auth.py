from copy import deepcopy
from utils.models import MAP_TO_COMMON_USER, User
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate as dj_auth
from django.contrib.auth import login as dj_login


def register_user_model(app):
    def decorator(klass):
        MAP_TO_COMMON_USER[app] = klass
        klass.get_token = _get_token
        klass.username = property(lambda self: self.user.username)
        klass.create_new = _set_app(app)
        return klass

    return decorator


def _set_app(key):
    return lambda is_superuser=False, **kwargs: _create_new(
        app=key, is_superuser=is_superuser, **kwargs
    )


def _get_token(self):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(self.user)
    token = jwt_encode_handler(payload)
    return token


def _create_new(app=None, is_superuser=False, **kwargs):
    is_superuser |= kwargs.pop('is_superuser', False)
    credentials = dict(
        username=kwargs.pop('username'),
        password=kwargs.pop('password'),
    )

    User.objects.__getattribute__(
        f'create_{"super" if is_superuser else ""}user'
    )(**credentials)
    related_user = User.objects.get(username=credentials['username'])

    MAP_TO_COMMON_USER[app].objects.create(
        user=related_user,
        **kwargs
    )


def authenticate(username, password, app):
    qs = MAP_TO_COMMON_USER[app].objects.filter(
        user=dj_auth(
            username=username,
            password=password,
        )
    )

    return qs.first() if qs.count() == 1 else None


def login(request, user, backend=None):
    return dj_login(
        request,
        user if isinstance(user, User) else user.user,
        backend
    )
