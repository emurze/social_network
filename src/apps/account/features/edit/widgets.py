from django.forms import ClearableFileInput


class MyPhoto(ClearableFileInput):
    template_name = "account/edit/form/photoWidget/photoWidget.html"
