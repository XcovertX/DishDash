from django.urls import path
from .views import recipe_list, recipe_detail

urlpatterns = [
    path('', recipe_list, name='recipe_list'),
    path('<int:pk>/', recipe_detail, name='recipe_detail'),
    # Add other URL patterns for creating, updating, and deleting recipes
]