from django.db import models
from django.contrib.auth.models import AbstractUser

MAP_TO_COMMON_USER = dict()


class User(AbstractUser):

    fields = (
        'username',
        'email',
        'is_active',
        'is_staff',
        'is_superuser',
    )
