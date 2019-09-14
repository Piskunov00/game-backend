from django import forms


class CreateGameForm(forms.Form):
    type = forms.IntegerField(min_value=0, max_value=1)


class JoinGameForm(forms.Form):
    string_invite = forms.IntegerField(min_value=1000, max_value=9999)


class BeginGameForm(forms.Form):
    duration = forms.IntegerField(min_value=1)  # в секундах


class UpdateStateForm(forms.Form):
    latitude = forms.FloatField()
    longitude = forms.FloatField()
    messages = forms.IntegerField(required=False, initial=0)
    coins = forms.IntegerField(required=False, initial=0)


class SendMessageForm(forms.Form):
    text = forms.CharField(max_length=1024)


class KickPlayerForm(forms.Form):
    target = forms.CharField()


class ChangeRadiusForm(forms.Form):
    cost = forms.IntegerField()
    radius = forms.IntegerField()
