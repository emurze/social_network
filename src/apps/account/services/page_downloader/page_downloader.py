import logging
from dataclasses import dataclass, field

from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render

lg = logging.getLogger(__name__)


@dataclass
class PageQuerySetDownloader:
    request: WSGIRequest
    page: int
    queryset: QuerySet
    per_page_count: int
    context_object_name: str
    template_name: str
    mixins: list | tuple = field(default_factory=tuple)
    extra_context: dict = field(default_factory=dict)

    def _get_queryset(self) -> QuerySet | HttpResponse:
        paginator = Paginator(self.queryset, self.per_page_count)
        try:
            queryset = paginator.page(self.page)
        except (EmptyPage, PageNotAnInteger):
            return HttpResponse('')

        return queryset

    def _get_context(self, queryset: QuerySet) -> dict:
        context_object_name = self.context_object_name

        class Returns:
            def get_context_data(self, **kwargs):
                if not kwargs.get(context_object_name):
                    kwargs[context_object_name] = self.object_list
                return kwargs

        class ClassToFunc(*self.mixins, Returns):
            object_list = queryset
            request = self.request

        context = ClassToFunc().get_context_data()
        return context

    def extend_context(self, extra_context: dict) -> None:
        self.extra_context |= extra_context

    def render(self) -> HttpResponse:
        queryset: QuerySet | HttpResponse = self._get_queryset()

        if isinstance(queryset, HttpResponse):
            return queryset

        context = self._get_context(queryset) | self.extra_context
        return render(self.request, self.template_name, context)
