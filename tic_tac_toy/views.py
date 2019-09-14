import logging
from string import Template

from django.views import View
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.status import *
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import jwt_get_username_from_payload

from tic_tac_toy.forms import RegistrationForm
from tic_tac_toy.models import (
    Player,
    Invite,
)

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
logger = logging.getLogger(__name__)


class Login(View):
    """
    Get - вход;
    Post - регистрация (получение инвайт ссылки на активацию)
    """
    egg = None
    invite = None
    text_invite = Template(
        'Hello from Tic-Tac-Toy!\n'
        'To confirm this is correct, go to $host/$path/$slug/\n'
        'Thank you from CS Academy!\n'
        'Regards, $host'
    )

    def get(self, request):
        token = dict(request.headers).get('Token')
        username = request.GET.get('username', None)
        password = request.GET.get('password', None)

        if token:
            self._login_by_token(token)
        elif username and password:
            self._login_by_credentions(username, password)
        else:
            return HttpResponse(
                status=HTTP_400_BAD_REQUEST,
            )
    def _login_by_token(self, token):
        try:
            payload = jwt_decode_handler(token)
            username = jwt_get_username_from_payload(payload)
            return Player.objects.get(user__username=username)
        except Exception as e:
            logger.exception(e)
            return HttpResponse(
                status=HTTP_400_BAD_REQUEST,
            )

    def _login_by_credentials(self, username, password):
        try:
            Player.objects.get(
                user__username=username,
                password=password,
            )

            # todo: избавиться от дублирования
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(player)
            token = jwt_encode_handler(payload)

            return HttpResponse(
                status=HTTP_200_OK,
                content=token,
            )
        except Exception as e:
            logger.exception(e)
            return HttpResponse(
                status=HTTP_404_NOT_FOUND,
            )

    def post(self, request):
        form = RegistrationForm(request.POST)
        if not form.is_valid():
            return HttpResponse(
                status=HTTP_400_BAD_REQUEST,
            )

        data = form.cleaned_data
        self.egg = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            email=data['email'],
            is_active=False,
        )
        self.egg.save()
        self._generate_invite()
        return self._send_to_email()

    def _generate_invite(self):
        self.invite = Invite(
            target=self.egg,
        )
        self.invite.save()

    def _send_to_email(self):
        result = send_mail(
            '[ifrag] Confirm E-mail Address',
            self.text_invite.substitute(
                slug=self.invite.slug,
                host=settings.CUR_HOST,
                path='invite',
            ),
            settings.EMAIL_HOST_USER,
            [self.egg.email],
            fail_silently=False,
        )
        return HttpResponse(
            status={
                1: HTTP_201_CREATED
            }.get(result, HTTP_500_INTERNAL_SERVER_ERROR)
        )


class InviteView(View):
    def get(self, slug):

        invite = get_object_or_404(Invite, slug=slug)
        user = invite.target.user
        user.is_active = True
        user.save()

        return HttpResponse('Ok')
