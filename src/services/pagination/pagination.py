import logging

from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, Page
from django.db.models import QuerySet
from django.http import HttpResponse

lg = logging.getLogger(__name__)


class PaginationMixin:
    object_list: QuerySet | None = None
    c_paginator: Paginator | None = None
    c_page: Page | None = None

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
        self.c_paginator = Paginator(self.object_list, self.paginate_by)
        try:
            self.c_page = self.c_paginator.page(page)
            lg.debug(f'page {self.c_page}')
        except PageNotAnInteger:
            pass
        except EmptyPage:
            return HttpResponse('')

        context = self.get_context_data()
        return self.render_to_response(context)

    def paginate_queryset(self, queryset, page_size):
        return (
            self.c_paginator,
            self.c_page,
            self.c_page.object_list,
            self.c_page.has_other_pages()
        )
