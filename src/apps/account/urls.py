from django.urls import path

from apps.account.features.edit.views import AccountEditView
from apps.account.features.detail.views import AccountDetailView, follow_detail
from apps.account.features.list.views import AccountListView, follow_list

app_name = 'account'

urlpatterns = [
    path('profile/edit_window/<slug:username>/', AccountEditView.as_view(),
         name='edit_window'),
    path('users/', AccountListView.as_view(), name='users'),
    path('profile/<slug:username>/', AccountDetailView.as_view(),
         name='detail'),
    path('profile/<slug:username>/follow/', follow_detail, name='follow'),
    path('profile/users/follows/', follow_list, name='follow_list')
]
