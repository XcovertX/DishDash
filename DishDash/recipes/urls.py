from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('', include('apps.recipes.urls')),
    path('admin/', admin.site.urls),
    path('recipes/', include('apps.recipes.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        # Serve static and media files in development.
        path('media/<path>', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        path('static/<path>', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    ]
