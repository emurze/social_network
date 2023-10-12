import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.views.generic import DetailView, UpdateView

from .forms import EditCoverForm, AccountEditForm
from .mixins import AddUserPosts, \
    AddFollowingUsersMixin, ProfileSelectedMixin, AjaxErrorsMixin, \
    AddFollowActionMixin, AddFollowingUsersPaginationMixin

from apps.post.pages.posts.mixins import AddReplyFormMixin, AddPostForm

User = get_user_model()
lg = logging.getLogger(__name__)


class AccountDetailView(
    LoginRequiredMixin,
    ProfileSelectedMixin,
    AddPostForm,
    AddReplyFormMixin,
    AddFollowActionMixin,
    AddFollowingUsersMixin,
    AddUserPosts,
    DetailView
):
    model = User
    template_name = 'account/profile/profile.html'
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = (
        User.objects
            .only(
                'id',
                'photo',
                'username',
                'is_staff',
                'description',
                'gender',
                'cover',
                'birthday',
            )
    )


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

    def get_queryset(self):
        username = self.kwargs.get('username')
        users = User.objects.filter(username=username).only('followings')

        if not users.exists():
            return User.followings.none()

        queryset = users.first().get_followings()

        return queryset.only(
            'photo',
            'gender',
            'is_staff',
            'username',
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
        return JsonResponse({'is_errors': True})
