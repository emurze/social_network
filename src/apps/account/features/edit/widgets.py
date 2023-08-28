from django.forms import ClearableFileInput


class MyPhoto(ClearableFileInput):
    template_name = "account/edit_window/form/photoWidget/photoWidget.html"
