from django.forms import ClearableFileInput


class MyPhoto(ClearableFileInput):
    template_name = "account/profile/edit_window/form/photoWidget/photoWidget.html"
