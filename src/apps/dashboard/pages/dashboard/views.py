from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET


@login_required
@require_GET
def dashboard(request: WSGIRequest) -> HttpResponse:
    template_name = 'dashboard/dashboard.html'
    context = {}
    return render(request, template_name, context)
