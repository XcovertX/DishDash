from django.shortcuts import render, get_object_or_404
from .models import Recipe
from django.shortcuts import render

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe_list.html', {'recipes': recipes})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipe_detail.html', {'recipe': recipe})

def home(request):
    return render(request, 'home.html')

# Add more views for creating, updating, and deleting recipes