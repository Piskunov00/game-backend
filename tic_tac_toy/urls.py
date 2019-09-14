from django.urls import path
from tic_tac_toy.views import *

app_name = 'tic_tac_toy'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('invite/<slug:slug>/', InviteView.as_view(), name='invite'),
]
