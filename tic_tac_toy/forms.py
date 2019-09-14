from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=3)
    password = forms.CharField(min_length=3)
    email = forms.EmailField()
