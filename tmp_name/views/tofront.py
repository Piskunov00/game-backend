from django.http import HttpResponse


def index(request):
    name = getattr(getattr(request, 'user', None), 'name', None)
    return HttpResponse(f'Hello{f", {name}," if name else ""} in GameWithNoName')

