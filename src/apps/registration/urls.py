from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from apps.registration.pages.login.forms import MyAuthForm
from apps.registration.pages.password_change.views import MyPasswordChangeView
from apps.registration.pages.password_reset.forms import MyPasswordResetForm
from apps.registration.pages.password_reset.views import MyPasswordResetView
from apps.registration.pages.password_reset_confirm.views import \
    MyPasswordResetConfirmView
from apps.registration.pages.registration.views import RegistrationView

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
         MyPasswordChangeView.as_view(),
         name='password_change'),

    path('password_reset/',
         MyPasswordResetView.as_view(
            form_class=MyPasswordResetForm,
         ),
         name='password_reset'),
    path('password_reset/<uidb64>/<token>/',
         MyPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('registration/', RegistrationView.as_view(), name='registration'),
]
