from .models import (
    Gamer,
    Game,
    BotGame,
    GiG,
    Coin,
    Message,
)
from django.contrib import admin
from utils.models import User


# Register your models here.
admin.site.register(User)
admin.site.register(Gamer)
admin.site.register(Game)
admin.site.register(BotGame)
admin.site.register(GiG)
admin.site.register(Coin)
admin.site.register(Message)
