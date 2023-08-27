from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from apps.registration.features.login.forms import MyAuthForm
from apps.registration.features.password_reset.forms import MyPasswordResetForm
from apps.registration.features.registration.views import RegistrationView

urlpatterns = [
    path('login/',
         auth_views.LoginView.as_view(
             authentication_form=MyAuthForm,
             next_page=reverse_lazy('dashboard')
         ),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(
             next_page=reverse_lazy('dashboard')
         ),
         name='logout'),

    path('password_change/',
         auth_views.PasswordChangeView.as_view(
             success_url=reverse_lazy('dashboard')
         ),
         name='password_change'),

    path('password_reset/',
         auth_views.PasswordResetView.as_view(
            form_class=MyPasswordResetForm,
            success_url=reverse_lazy('dashboard')
         ),
         name='password_reset'),
    path('password_reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('dashboard')
         ),
         name='password_reset_confirm'),
    path('registration/', RegistrationView.as_view(), name='registration'),
]
