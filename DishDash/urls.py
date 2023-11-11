from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recipes/', include('apps.recipes.urls')),
    # Add other URL patterns for your project here
]
