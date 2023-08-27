from django.urls import path

from apps.dashboard.features.dashboard.views import dashboard

urlpatterns = [
    path('', dashboard),
    path('dashboard/', dashboard, name='dashboard'),
]
