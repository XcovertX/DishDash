from django.urls import include, path
from .views import recipe_list, recipe_detail, home, profile, signup, login, logout

urlpatterns = [
    path('recipes/', recipe_list, name='recipe_list'),
    path('<int:pk>/', recipe_detail, name='recipe_detail'),
    path('', home, name='home'),
    path('profile/', profile, name='profile'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]