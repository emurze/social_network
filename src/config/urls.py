from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('apps.registration.urls')),

    path('', include('apps.dashboard.urls')),
    path('', include('apps.account.urls', namespace='account')),
    path('', include('apps.post.urls', namespace='post')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        path('__debug__/', include(debug_toolbar.urls))
    ]


