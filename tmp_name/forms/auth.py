from django.contrib.auth.forms import UserCreationForm
from tmp_name.models import Gamer


class CustomUserCreationForm(UserCreationForm):  # todo: начать использовать форму

    class Meta(UserCreationForm.Meta):
        model = Gamer
        fields = ('name', )
