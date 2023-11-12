from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('apps.recipes.urls')),
    path('admin/', admin.site.urls),
    path('recipes/', include('apps.recipes.urls')),
]
