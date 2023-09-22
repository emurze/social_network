import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import DetailView, UpdateView

from .forms import EditCoverForm, AccountEditForm
from .mixins import AddUserPosts, LikeActionAccountDetailMixin, \
    AddFollowingUsersMixin, ProfileSelectedMixin, AjaxErrorsMixin, \
    FollowActionDetailMixin, AddFollowingUsersPaginationMixin

from apps.post.pages.posts.mixins import AddReplyFormMixin, AddPostForm

User = get_user_model()
lg = logging.getLogger(__name__)


class AccountDetailView(
    LoginRequiredMixin,
    ProfileSelectedMixin,
    FollowActionDetailMixin,
    AddFollowingUsersMixin,
    AddUserPosts,
    AddPostForm,
    AddReplyFormMixin,
    LikeActionAccountDetailMixin,
    DetailView
):
    model = User
    template_name = 'account/profile/profile.html'
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'


class AccountEditView(LoginRequiredMixin, AjaxErrorsMixin, UpdateView):
    model = User
    form_class = AccountEditForm
    template_name = 'account/profile/edit_window/edit_window.html'
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'


class FollowPagination(AddFollowingUsersPaginationMixin):
    template_name = (
        'account/profile/followings/followingContent/followingContent.html'
    )


class EditCover(UpdateView):
    model = User
    form_class = EditCoverForm
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def form_valid(self, form: EditCoverForm) -> HttpResponse:
        form.save()
        return HttpResponse('')

    def form_invalid(self, form: EditCoverForm) -> HttpResponse:
        lg.warning('User edit form without data.')
        return HttpResponse('')
