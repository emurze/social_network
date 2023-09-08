from django.urls import path

from apps.account.features.edit.views import AccountEditView
from apps.account.features.detail.views import AccountDetailView, \
    follow_detail, follow_pagination
from apps.account.features.list.views import AccountListView, follow_list, \
    download_users

app_name = 'account'

urlpatterns = [
    path('users/', AccountListView.as_view(), name='users'),
    path('dowload_users', download_users, name='download_users'),

    path('profile/edit_window/<slug:username>/', AccountEditView.as_view(),
         name='edit_window'),
    path('profile/follows/', follow_list, name='follow_list'),
    path('profile/<slug:username>/', AccountDetailView.as_view(),
         name='detail'),
    path('profile/<slug:username>/follow/', follow_detail, name='follow'),
    path('profile/follow_pagination/<int:user_id>/', follow_pagination,
         name='follow_pagination')
]
