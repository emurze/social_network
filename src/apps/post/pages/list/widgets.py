from django.forms import ClearableFileInput


class PostPhoto(ClearableFileInput):
    template_name = "post/posts/createPostForm/photoWidget/photoWidget.html"
