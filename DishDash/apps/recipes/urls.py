from django.urls import include, path
from .views import recipe_list, recipe_detail, home

urlpatterns = [
    path('recipes/', recipe_list, name='recipe_list'),
    path('<int:pk>/', recipe_detail, name='recipe_detail'),
    path('', home, name='home'), 
]