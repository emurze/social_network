from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.views.generic import ListView

User = get_user_model()
DEFAULT_USER_COUNT = 18


class AccountListView(ListView):
    template_name = 'account/users/users.html'
    context_object_name = 'users'

    def get_queryset(self) -> QuerySet[User]:
        # return (User.objects
        #             .order_by('username')
        #             .exclude(id=self.request.user.id))[:DEFAULT_USER_COUNT]
        return User.objects.order_by('username')
