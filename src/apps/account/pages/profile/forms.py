import logging

from django import forms
from django.contrib.auth import get_user_model

from .widgets import MyPhoto

from utils.widgets.birthday_date import BirthdayDateWidget

User = get_user_model()
lg = logging.getLogger(__name__)


class EditCoverForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('cover',)


class AccountEditForm(forms.ModelForm):
    photo = forms.ImageField(label='Avatar', widget=MyPhoto, required=False)
    username = forms.CharField(
        required=True,
        label='Username',
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
        })
    )
    birthday = forms.DateField(required=True, widget=BirthdayDateWidget)
    gender = forms.ChoiceField(label='Gender',
                               widget=forms.RadioSelect,
                               choices=User.Gender.choices)
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={'rows': 4, 'maxlength': 120}),
        required=False
    )

    class Meta:
        model = User
        fields = ('username', 'description', 'birthday', 'gender', 'photo')

    def __init__(self, *args, **kwargs):

        MyPhoto.current_user = kwargs.get('instance')

        self.photo = forms.ImageField(
            label='Avatar',
            widget=MyPhoto,
            required=False
        )

        super().__init__(*args, **kwargs)

    def clean_username(self) -> str:
        cd = self.cleaned_data

        username = cd.get('username')
        if len(username) > 25:
            raise forms.ValidationError('Username should be less then 26')

        return username

    def clean_description(self) -> str:
        cd = self.cleaned_data

        description = cd.get('description')
        if len(description) > 120:
            raise forms.ValidationError('Description should be less then 120')

        return description
