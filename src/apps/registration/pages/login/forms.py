from django import forms
from django.contrib.auth.forms import UsernameField, AuthenticationForm


class MyAuthForm(AuthenticationForm):
    username = UsernameField(
        label='Username or email address',
        widget=forms.TextInput(attrs={
            "autofocus": True,
        })
    )
