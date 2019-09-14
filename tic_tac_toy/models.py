from django.db import models
from utils.models import User
from utils.auth import register_user_model


@register_user_model(app='tic-tac-toy')
class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)


class Game(models.Model):
    players = models.ManyToManyField(User)
    state = models.BigIntegerField()


class Invite(models.Model):
    target = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=30, unique=True, auto_created=True)
