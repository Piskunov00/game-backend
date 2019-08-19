from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import api.views.tofront
import api.views.outgame


urlpatterns = [
    path('', include('api.urls')),

    path("", api.views.tofront.index, name="index"),
    path("admin/", admin.site.urls),
]
