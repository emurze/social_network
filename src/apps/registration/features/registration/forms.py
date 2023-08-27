import logging

from django import forms
from django.contrib.auth import get_user_model

from utils.widgets.birthday_date import BirthdayDateWidget

User = get_user_model()
lg = logging.getLogger(__name__)


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'})
    )
    birthday = forms.DateField(required=True, widget=BirthdayDateWidget)
    gender = forms.ChoiceField(label='Gender',
                               widget=forms.RadioSelect,
                               choices=User.Gender.choices)

    class Meta:
        model = User
        fields = ('username', 'email', 'password',
                  'password2', 'birthday', 'gender')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }

    def clean_password(self):
        cd = self.cleaned_data

        if len(self.errors):
            return cd.get('password2')

        if len(cd.get('password')) < 8:
            raise forms.ValidationError("Passwords length less than 8")

        return cd.get('password')

    def clean_password2(self):
        cd = self.cleaned_data

        if len(self.errors):
            return cd.get('password2')

        if cd.get('password2') != cd.get('password'):
            raise forms.ValidationError("Passwords didn't match.")

        return cd.get('password2')
