from django.urls import path

from apps.dashboard.pages.dashboard.views import ActionList

urlpatterns = [
    path('', ActionList.as_view()),
    path('dashboard/', ActionList.as_view(), name='dashboard'),
]
