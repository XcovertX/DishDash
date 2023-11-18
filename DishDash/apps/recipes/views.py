from django.shortcuts import render, get_object_or_404
from .models import Recipe, UserProfile, Rating, Comment, User, Follow
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MyLoginForm, UserProfileForm, UserForm, RatingForm, RecipeForm, CommentForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe_list.html', {'recipes': recipes})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    comments = Comment.objects.filter(recipe=recipe, parent_comment=None).prefetch_related('replies')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                parent_comment_id = request.POST.get('parent_comment')
                Comment.objects.create(user=request.user, text=form.cleaned_data['text'],
                                    recipe=recipe, parent_comment_id=parent_comment_id)
    else:
        form = CommentForm()
    user_rating = Rating.objects.filter(user=request.user, recipe=recipe).first()
    recipe.increase_views()
    context = {
        'recipe': recipe, 
        'user_rating': user_rating,
        'comment_form': form,
        'comments': comments
    }
    return render(request, 'recipe_detail.html', context)

def render_comment_form(request, recipe_id, parent_comment_id=None):
    recipe = Recipe.objects.get(pk=recipe_id)
    parent_comment = Comment.objects.get(pk=parent_comment_id) if parent_comment_id else None
    form = CommentForm()
    return render(request, 'comment_form.html', {'recipe': recipe, 'parent_comment': parent_comment, 'comment_form': form})

def reply_comment(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_comment_id = request.POST.get('parent_comment')
            parent_comment = Comment.objects.get(pk=parent_comment_id) if parent_comment_id else None
            Comment.objects.create(user=request.user, text=form.cleaned_data['text'],
                                   recipe=recipe, parent_comment=parent_comment)
    return redirect('recipe_detail', recipe_id=recipe.id)

@csrf_exempt
def like_comment(request, comment_id):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            comment = Comment.objects.get(pk=comment_id)
            if user in comment.likes.all():
                return JsonResponse({
                    'status': 'liked'
                    })
            else:
                return JsonResponse({'status': 'not_liked'})
        else:
            return JsonResponse({'status': 'not_authenticated'})
    elif request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            comment = Comment.objects.get(pk=comment_id)
            if user not in comment.likes.all():
                comment.likes.add(user)
                comment.dislikes.remove(user)  # Remove dislike if user had disliked before
                print(comment.likes.all().count(), comment.dislikes.all().count())
                return JsonResponse({
                    'status': 'liked',
                    'likes': comment.likes.all().count(),
                    'dislikes': comment.dislikes.all().count()
                    })
            else:
                return JsonResponse({'status': 'already_liked'})

        return JsonResponse({'status': 'not_authenticated'})
    else:
        return JsonResponse({'error': 'Invalid request'})
    
@csrf_exempt
def dislike_comment(request, comment_id):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            comment = Comment.objects.get(pk=comment_id)
            if user in comment.dislikes.all():
                return JsonResponse({
                    'status': 'disliked'
                    })
            else:
                return JsonResponse({'status': 'not_disliked'})
        else:
            return JsonResponse({'status': 'not_authenticated'})
    elif request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            comment = Comment.objects.get(pk=comment_id)
            if user not in comment.dislikes.all():
                comment.dislikes.add(user)
                comment.likes.remove(user)  # Remove dislike if user had disliked before
                return JsonResponse({
                    'status': 'disliked',
                    'likes': comment.likes.all().count(),
                    'dislikes': comment.dislikes.all().count()
                    })
            else:
                return JsonResponse({'status': 'already_disliked'})

        return JsonResponse({'status': 'not_authenticated'})
    else:
        return JsonResponse({'error': 'Invalid request'})

@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            new_recipe        = form.save(commit=False)
            new_recipe.user   = request.user
            new_recipe.save()
            return redirect('recipe_detail', recipe_id=new_recipe.id)
        else: 
            print(form.errors)
    else:
        form = RecipeForm()

    return render(request, 'create_recipe.html', {'form': form})

def home(request):
    trending_recipes = Recipe.objects.order_by('-views')[:5].select_related('user')
    return render(request, 'home.html', {'trending_recipes': trending_recipes})

def profile(request):
    user_recipes = Recipe.objects.filter(user=request.user)
    context = {
        'user': request.user,
        'user_recipes': user_recipes,
    }
    
    return render(request, 'profile.html', context)

def edit_profile(request):
    user = request.user 
    if request.method == 'POST':
        user_form     = UserForm(request.POST, instance=user)
        profile_form  = UserProfileForm(request.POST, request.FILES, instance=user)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form    = UserForm(instance=user)
        profile_form = UserProfileForm(instance=user)

    context = {
        'user': user,
        'user_form': user_form, 
        'profile_form': profile_form
    }
    return render(request, 'edit_profile.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            auth_login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next', 'profile'))  # Redirect to 'profile' or a default URL
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def rate_recipe(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    user_rating, created = Rating.objects.get_or_create(user=request.user, recipe=recipe)

    if request.method == 'POST':
        form = RatingForm(request.POST, instance=user_rating)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', recipe_id=recipe_id)
    else:
        form = RatingForm(instance=user_rating)

    context = {
        'recipe': recipe,
        'form': form,
    }

    return render(request, 'rate_recipe.html', context)

@login_required
def follow_user(request, user_id):
    user_to_follow = User.objects.get(pk=user_id)
    if request.user.is_authenticated:
        if user_to_follow != request.user:
            if request.user.following.filter(following=user_to_follow).exists():
                request.user.following.filter(following=user_to_follow).delete()
                return JsonResponse({'status': 'unfollowed'})
            else:
                Follow.objects.create(follower=request.user, following=user_to_follow)
                return JsonResponse({'status': 'followed'})
        else:
            return JsonResponse({'status': 'cannot_follow_self'})
    else:
        return JsonResponse({'status': 'not_authenticated'})
