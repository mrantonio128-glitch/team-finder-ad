"""Team finder URL configuration."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

from projects.views import index_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    # redirect
    path('', index_redirect, name='index'),
    path('projects/', include('projects.urls')),
    path('users/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.BASE_DIR / 'static'
    )
else:
    # hack for debug = false
    urlpatterns += [
        path(
            'media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}
        ),
    ]
