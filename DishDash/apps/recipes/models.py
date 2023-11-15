from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    ingredients = models.JSONField()
    instructions = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    def __str__(self):
        return self.user.username
