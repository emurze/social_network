from django.urls import path

from apps.account.pages.profile.views import AccountDetailView, \
    AccountEditView, follow_detail, FollowPagination, edit_cover
from apps.account.pages.users.views import (
    AccountListView,
    follow_list,
    FilterUsers,
    SearchUsers,
    DownloadUsers,
)

app_name = 'account'

urlpatterns = [
    path('users/', AccountListView.as_view(), name='users'),
    path('users/download/', DownloadUsers.as_view(), name='download_users'),
    path('users/filter/', FilterUsers.as_view(), name='filter_users'),
    path('users/search/', SearchUsers.as_view(), name='search_users'),

    path('profile/follows/', follow_list, name='follow_list'),
    path('profile/follow_pagination/',
         FollowPagination.as_view(),
         name='follow_pagination'),
    path('profile/edit_window/<slug:username>/', AccountEditView.as_view(),
         name='edit_window'),

    path('profile/<slug:username>/', AccountDetailView.as_view(),
         name='detail'),
    path('profile/<slug:username>/edit_cover/', edit_cover, name='edit_cover'),
    path('profile/<slug:username>/follow/', follow_detail, name='follow'),
]
