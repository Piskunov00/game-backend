from django.urls import path, include

from django.contrib import admin

from tmp_name.views import (
    tofront,
    outgame,
)


admin.autodiscover()

urlpatterns = [
    path('tmp_name/', include('tmp_name.urls', namespace='tmp_name')),
    path('tic-tac-toy/', include('tic_tac_toy.urls', namespace='tic_tac_toy')),

    path("", tofront.index, name="index"),
    path("admin/", admin.site.urls),
]
