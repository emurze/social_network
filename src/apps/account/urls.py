from django.urls import path

from apps.account.features.edit.views import AccountEditView
from apps.account.features.detail.views import AccountDetailView
from apps.account.features.list.views import AccountListView

app_name = 'account'

urlpatterns = [
    path('profile/edit/<slug:username>/', AccountEditView.as_view(),
         name='edit'),
    path('users/', AccountListView.as_view(), name='list'),
    path('profile/<slug:username>/', AccountDetailView.as_view(),
         name='detail'),
]
