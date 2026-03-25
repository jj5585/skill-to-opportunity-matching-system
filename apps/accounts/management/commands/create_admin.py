from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a superuser non-interactively'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        email = 'admin@skillsync.com'
        password = 'ChangeMe123!'
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email, password=password)
            self.stdout.write(f'Superuser created: {email}')
        else:
            self.stdout.write('Superuser already exists')
