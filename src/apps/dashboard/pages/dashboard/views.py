from apps.dashboard.models import Action
from apps.dashboard.pages.dashboard.mixins import (
    ActionLimitQuerysetMixin, ActionListMixin, ActionCountersMixin
)


class ActionList(
    ActionLimitQuerysetMixin,
    ActionCountersMixin,
    ActionListMixin,
):
    template_name = 'dashboard/dashboard.html'
    queryset = (
        Action.objects
              .select_related('user', 'content_type')
              .prefetch_related(
                  'content_object',
              ).only(
                  'created',
                  'verb',
                  'user__username',
                  'user__photo',
                  'object_id',
                  'content_type_id',
                  'content_type__model',
                  'content_type__app_label',
              )
    )
