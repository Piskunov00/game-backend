import logging

logger = logging.getLogger(__name__)


class MyTokenMiddleware:
    """
    В request.user положу Gamer
     * если в хидерах передали token
     * если token соответствует пользователю
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if request.headers.get('Token'):
                from api.utils.http_ import auth_with_token
                token = request.headers.get('Token')
                user = auth_with_token(token)
                if user:
                    logger.info(f'Successful login with {user.name} user token')
                    request.user = user
        except Exception as e:
            logger.info(f'Token Login Failed {e}')

        response = self.get_response(request)
        return response
