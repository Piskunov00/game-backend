from django.http import HttpResponseBadRequest


class HttpRequestException(BaseException):
    """
    Подними это исключение, чтобы вернуться во view и отправить ответ
    """
    def __init__(self, *args, **kwargs):
        # todo: логировать варнинг если подменяют код ошибки
        self.reason = kwargs.get('reason', '')
        self.class_response = kwargs.get('class_error', HttpResponseBadRequest)
        self.status = kwargs.get('status', self.class_response.status_code)
        self.ready_response = kwargs.get('ready_response')

    @property
    def response(self):
        if self.ready_response:
            return self.ready_response
        return self.class_response(
            reason=self.reason,
            status=self.status,
        )