from django import forms

from apps.post.models import Reply


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('content', 'parent')
        widgets = {
            'content': forms.TextInput(
                attrs={
                    'placeholder': 'Post your reply...',
                    'autocomplete': "off",
                }
            ),
            'parent': forms.HiddenInput,
        }
