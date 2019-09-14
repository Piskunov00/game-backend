from django import forms


class CreateGameWithBot(forms.Form):
    alpha = forms.IntegerField(min_value=0)
    speed = forms.IntegerField(min_value=1)
    begin_latit = forms.FloatField()
    begin_long = forms.FloatField()
    end_latit = forms.FloatField()
    end_long = forms.FloatField()


class UpdateGameWithBot(forms.Form):
    latitude = forms.FloatField()
    longitude = forms.FloatField()
    update_dist = forms.BooleanField()
