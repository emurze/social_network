from django.urls import path

from apps.account.pages.detail.views import AccountDetailView, \
    AccountEditView, follow_detail, follow_pagination, edit_cover
from apps.account.pages.list.views import AccountListView, follow_list, \
    download_users, filter_users, search_users

app_name = 'account'

urlpatterns = [
    path('users/', AccountListView.as_view(), name='users'),
    path('users/download/', download_users, name='download_users'),
    path('users/filter/', filter_users, name='filter_users'),
    path('users/search/', search_users, name='search_users'),

    path('profile/follows/', follow_list, name='follow_list'),
    path('profile/follow_pagination/<int:user_id>/', follow_pagination,
         name='follow_pagination'),
    path('profile/edit_window/<slug:username>/', AccountEditView.as_view(),
         name='edit_window'),

    path('profile/<slug:username>/', AccountDetailView.as_view(),
         name='detail'),

    path('profile/<slug:username>/edit_cover/', edit_cover, name='edit_cover'),
    path('profile/<slug:username>/follow/', follow_detail, name='follow'),
]
