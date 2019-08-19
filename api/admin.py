from .models import (
    Gamer,
    Game,
    BotGame,
    GiG,
    Coin,
    Message,
)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# Register your models here.
admin.site.register(Gamer)
admin.site.register(Game)
admin.site.register(BotGame)
admin.site.register(GiG)
admin.site.register(Coin)
admin.site.register(Message)


# Define an inline admin descriptor for Gamer model
# which acts a bit like a singleton
class GamerInline(admin.StackedInline):
    model = Gamer
    can_delete = False
    verbose_name_plural = 'Gamers'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (GamerInline,)


# Re-register UserAdmin
# admin.site.unregister(Gamer)
# admin.site.register(User, UserAdmin)
