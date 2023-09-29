from django import forms
from django.contrib.auth.forms import PasswordResetForm


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "Email",
                "placeholder": "Email",
                "autofocus": True,
            }
        ),
    )
