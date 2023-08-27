from django import forms
from django.contrib.auth import get_user_model

from utils.widgets.birthday_date import BirthdayDateWidget
from apps.account.features.edit.widgets import MyPhoto

User = get_user_model()


class AccountEditForm(forms.ModelForm):
    photo = forms.ImageField(label='Avatar', widget=MyPhoto, required=False)
    username = forms.CharField(required=True, label='Username')
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
