from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Recipe(models.Model):
    id           = models.AutoField(primary_key=True)
    title        = models.CharField(max_length=255)
    ingredients  = models.JSONField()
    instructions = models.JSONField()
    created_at   = models.DateTimeField(auto_now_add=True)
    @property
    def average_rating(self):
        return self.rating_set.aggregate(Avg('stars'))['stars__avg']

    def __str__(self):
        return self.title

class Rating(models.Model):
    user   = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    stars  = models.IntegerField(default=0, choices=[(i, str(i)) for i in range(1, 6)])

class UserProfile(models.Model):
    user   = models.OneToOneField(User, on_delete=models.CASCADE)
    bio    = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    def __str__(self):
        return self.user.username
