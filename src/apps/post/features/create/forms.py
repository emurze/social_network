from django import forms

from apps.post.features.create.widgets import PostPhoto
from apps.post.models import Post


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
