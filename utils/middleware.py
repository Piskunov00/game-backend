import logging
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import jwt_get_username_from_payload

logger = logging.getLogger(__name__)
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class MyTokenMiddleware:
    """
    В request.user положу User
     * если в хидерах передали token
     * если token соответствует пользователю
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if request.headers.get('Token'):
                token = request.headers.get('Token')
                user = auth_with_token(token)
                if user:
                    logger.info(f'Successful login with {user.username} user token')
                    request.user = user
            else:
                logger.info("Request without token")
        except Exception as e:
            logger.warning(f'Token Login Failed {e}')

        response = self.get_response(request)
        return response


def auth_with_token(token):
    try:
        from utils.models import User
        payload = jwt_decode_handler(token)
        username = jwt_get_username_from_payload(payload)
        return User.objects.get(username=username)
    except Exception as e:
        logger.info(f'logging failed with error={e}, token={token}')
