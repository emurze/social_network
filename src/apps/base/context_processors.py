import os

from django.core.handlers.wsgi import WSGIRequest


def site_settings(request: WSGIRequest) -> dict:
    return {'server_id': os.getenv('SERVER_ID', 0)}
