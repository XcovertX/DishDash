from django.shortcuts import render, get_object_or_404
from .models import Recipe, UserProfile, Rating
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MyLoginForm, UserProfileForm, UserForm, RatingForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe_list.html', {'recipes': recipes})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})

def home(request):
    return render(request, 'home.html')

def profile(request):
    user = request.user  # Assuming you have a one-to-one relationship

    context = {
        'user': request.user,
    }
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=user)
    
    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})

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
