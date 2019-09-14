from django.db import models
from utils.choicer import choicer
from utils.models import User
from utils.auth import register_user_model


@register_user_model(app='tmp_name')
class Gamer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    birthday = models.DateField(blank=True, null=True)
    date_sign_up = models.DateTimeField(auto_now_add=True)
    sex = models.IntegerField(blank=True, null=True, default=0)
    money = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    mileage = models.IntegerField(default=0)
    hints = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class Game(models.Model):
    @choicer
    class StatusGameChoices:
        CREATED = 'CR'
        INITIALIZED = 'IN'
        STARTED = 'ST'
        FINISHED = 'FN'
        ARCHIVED = 'AR'
        _order = [CREATED, INITIALIZED, STARTED, FINISHED, ARCHIVED]

    link = models.CharField(unique=True, max_length=4)
    duration = models.IntegerField(null=True)
    type_game = models.IntegerField()

    # для более быстрого доступа к self.players.count()
    cnt_gamers = models.IntegerField(default=0)

    status = models.CharField(
        max_length=2,
        choices=StatusGameChoices.as_list(),
        default='CR',
    )
    time_end_game = models.IntegerField(null=True)
    players = models.ManyToManyField(Gamer, through='GiG')

    def __str__(self):
        return f'Game-{self.link}'


class BotGame(models.Model):
    gamer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    date = models.IntegerField()
    alpha = models.IntegerField()
    speed = models.FloatField()
    path = models.IntegerField()
    cnt_stops = models.IntegerField()
    begin_latit = models.FloatField()
    begin_long = models.FloatField()
    end_latit = models.FloatField()
    end_long = models.FloatField()
    user_latit = models.FloatField()
    user_long = models.FloatField()

    def __str__(self):
        return '{}\'s game'.format(self.gamer.name)


class GiG(models.Model):
    @choicer
    class StatusGiGChoices:
        ACTIVE = 'AC'
        DISCONNECTED = 'NA'
        BLOCKED = 'BL'
        _order = ['BL', 'NA', 'AC']

    gamer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.CharField(
        max_length=2,
        choices=StatusGiGChoices.as_list(),
        default='AC',
    )
    color = models.IntegerField()
    radius = models.IntegerField(null=True)
    chief = models.BooleanField(default=False)

    def __str__(self):
        return '{}-{}'.format(self.gamer, self.game)


class Coin(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    latitude = models.FloatField(null=False, blank=False)
    longitude = models.FloatField(null=False, blank=False)
    cost = models.IntegerField(default=1)
    size = models.IntegerField(default=15)
    taken = models.BooleanField(default=False)
    whom = models.ForeignKey(Gamer, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '{} in {}'.format(self.id, self.game)


class Message(models.Model):
    gg = models.ForeignKey(GiG, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} in {}'.format(self.id, self.gg)


StatusGameChoices = Game.StatusGameChoices
StatusGiGChoices = GiG.StatusGiGChoices
