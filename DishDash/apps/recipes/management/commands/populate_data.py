import random
from django.core.management.base import BaseCommand
from apps.recipes.models import User, Recipe, Rating, Comment
from faker import Faker
import factory
import random
import json

fake = Faker()

class Command(BaseCommand):
    help = 'Populate your app with sample data'
    
    def handle(self, *args, **options):
        users = []
        for _ in range(5):
            firstname = fake.first_name()
            lastname  = fake.last_name()
            username  = fake.user_name()
            email     = fake.email()
            password  = fake.password()

            user = User.objects.create(
                first_name=firstname,
                last_name=lastname,
                username=username,
                email=email,
                password=password
            )
            users.append(user)
            self.stdout.write(self.style.SUCCESS(f'Successfully created user: {username}'))

        # Create recipes, ratings, and comments
        for user in users:
            for _ in range(10):  # Create 10 recipes per user
                recipe = Recipe.objects.create(
                    user=user,
                    title=fake.text(5),
                    description=fake.text(30),
                    ingredients = [fake.text(5) for _ in range(6)],
                    instructions = [fake.text(20) for _ in range(10)] 
                )

                # Generate random ratings
                for _ in range(random.randint(5, 20)):
                    stars = random.randint(1, 5)
                    Rating.objects.create(
                        recipe=recipe,
                        user=random.choice(users),
                        stars=stars
                    )

                # Generate random comments
                for _ in range(random.randint(1, 5)):
                    Comment.objects.create(
                        recipe=recipe,
                        user=random.choice(users),
                        text=fake.text()
                    )
                self.stdout.write(self.style.SUCCESS(f'Successfully created recipe for user: {user.username}'))    