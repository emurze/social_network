from django.urls import path

from apps.account.pages.profile.views import (
    AccountDetailView,
    AccountEditView,
    FollowPagination,
    EditCover
)
from apps.account.pages.users.views import (
    AccountListView,
    follow_user,
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

    path('users_profile/follow_user/', follow_user, name='follow_user'),

    path('profile_features/<slug:username>/follow_pagination/',
         FollowPagination.as_view(),
         name='follow_pagination'),
    path('profile_features/edit_window/<slug:username>/',
         AccountEditView.as_view(),
         name='edit_window'),
    path('profile_features/edit_cover/<slug:username>/', EditCover.as_view(),
         name='edit_cover'),

    path('profile/<slug:username>/', AccountDetailView.as_view(),
         name='detail'),
]
