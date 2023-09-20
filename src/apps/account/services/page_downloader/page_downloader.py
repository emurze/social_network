import logging
from dataclasses import dataclass, field

from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render

lg = logging.getLogger(__name__)


@dataclass
class PaginationDownloader:
    page: int
    queryset: QuerySet
    per_page_count: int
    context_object_name: str

    def _get_queryset(self) -> QuerySet | HttpResponse:
        paginator = Paginator(self.queryset, self.per_page_count)
        try:
            queryset = paginator.page(self.page)
        except (EmptyPage, PageNotAnInteger):
            return HttpResponse('')
        return queryset

    def get_context(self) -> dict | HttpResponse:
        queryset: QuerySet | HttpResponse = self._get_queryset()

        if isinstance(queryset, HttpResponse):
            return queryset

        return {self.context_object_name: queryset}
