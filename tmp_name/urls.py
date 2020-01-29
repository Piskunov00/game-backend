from django.urls import path, re_path, include

from tmp_name.views import (
    onlinemode,
    gwbmods,
    outgame,
    tofront,
)

app_name = 'tmp_name'
urlpatterns = list()

OUTGAME_URLS = [
    ('change_show_hints/', outgame.change_show_hints),
    ('change_rating/', outgame.change_rating),
    ('get_top_users/', outgame.get_top_users),
    ('change_coins/', outgame.change_coins),
    ('show_users/', outgame.show_users),
    ('sign_in/', outgame.sign_in),
    ('sign_up/', outgame.sign_up),
]

ONLINE_MODE_URLS = [
    ('update_state_game/', onlinemode.update_state_game),
    ('change_radius/', onlinemode.change_radius),
    ('kill_run_game/', onlinemode.kill_run_game),
    ('send_message/', onlinemode.send_message),
    ('kick_player/', onlinemode.kick_player),
    ('create_game/', onlinemode.create_game),
    ('check_game/', onlinemode.check_game),
    ('begin_game/', onlinemode.begin_game),
    ('init_game/', onlinemode.init_game),
    ('join_game/', onlinemode.join_game),
]

GWB_MODE_URLS = [
    ('get_my_speed_gwb/', gwbmods.get_my_speed_gwb),
    ('stop_in_gwb/', gwbmods.stop_in_gwb),
    ('create_gwb/', gwbmods.create_gwb),
    ('update_gwb/', gwbmods.update_gwb),
    ('check_gwb/', gwbmods.gwb_detail),
    ('kill_gwb/', gwbmods.kill_gwb),
]

for package in [OUTGAME_URLS, ONLINE_MODE_URLS, GWB_MODE_URLS]:
    for pattern, view in package:
        urlpatterns.append(path(pattern, view))

from test_engine import views
urlpatterns.append(path('qwe', views.check_headers))
