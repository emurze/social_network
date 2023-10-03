from django.contrib.auth.views import PasswordResetView


class MyPasswordResetView(PasswordResetView):
    # def get_success_url(self):
    #     self.request.user if Anonymous then settings.login_url else base
    pass

