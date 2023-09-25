from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import QuerySet
from django.http import HttpResponse


class PaginationMixin:
    object_list: QuerySet | None = None

    def get(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                    self.object_list, "exists"
            ):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                return HttpResponse('')

        page = request.GET.get('page')
        paginator = Paginator(self.object_list, self.paginate_by)
        try:
            paginator.page(page)
        except PageNotAnInteger:
            pass
        except EmptyPage:
            return HttpResponse('')

        context = self.get_context_data()
        return self.render_to_response(context)

