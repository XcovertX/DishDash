from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from .views import follow_user, recipe_list, recipe_detail, home, profile, signup, login, logout, rate_recipe, create_recipe, edit_profile, reply_comment, like_comment, dislike_comment

urlpatterns = [
    path('recipes/', recipe_list, name='recipe_list'),
    path('', home, name='home'),
    path('profile/', profile, name='profile'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('rate_recipe/<int:recipe_id>/', rate_recipe, name='rate_recipe'),
    path('recipes/<int:recipe_id>/', recipe_detail, name='recipe_detail'),
    path('create_recipe/', create_recipe, name='create_recipe'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('recipes/<int:recipe_id>/reply_comment/', reply_comment, name='reply_comment'),
    path('like_comment/<int:comment_id>/', like_comment, name='like_comment'),
    path('dislike_comment/<int:comment_id>/', dislike_comment, name='dislike_comment'),
    path('follow/<int:user_id>/', follow_user, name='follow_user')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)