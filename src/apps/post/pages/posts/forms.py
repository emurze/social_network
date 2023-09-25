from django import forms

from apps.post.models import Reply, Post
from .widgets import PostPhoto


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


class PostForm(forms.ModelForm):
    photo = forms.ImageField(widget=PostPhoto, required=False)

    class Meta:
        model = Post
        fields = ('description', 'photo')
        widgets = {
            'description': forms.Textarea(
                attrs={
                    'rows': 9,
                    'placeholder': 'What is happening?!',
                    'maxlength': '280',
                }
            )
        }
