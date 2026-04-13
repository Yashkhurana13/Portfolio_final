from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = "Create superuser from environment variables"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.environ.get("USERNAME")
        email = os.environ.get("EMAIL")
        password = os.environ.get("PASSWORD")

        if not username or not email or not password:
            self.stdout.write("Missing environment variables")
            return

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write("Superuser created")
        else:
            self.stdout.write("Superuser already exists")
