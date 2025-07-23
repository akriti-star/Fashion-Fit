from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a test regular user for testing logout functionality'

    def handle(self, *args, **options):
        # Create a regular user (non-superuser)
        if not User.objects.filter(username='testuser').exists():
            user = User.objects.create_user(
                username='testuser',
                email='test@fashionfit.com',
                password='testpass123',
                first_name='Test',
                last_name='User',
                height_cm=170,
                weight_kg=65,
                body_type='athletic',
                gender='male'
            )
            self.stdout.write(self.style.SUCCESS(f'Created regular user: testuser (password: testpass123)'))
        else:
            self.stdout.write(self.style.WARNING('Regular user "testuser" already exists'))
        
        # Check if superuser exists
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.SUCCESS('Superuser "admin" exists (password: admin123)'))
        else:
            self.stdout.write(self.style.WARNING('Superuser "admin" does not exist'))
        
        self.stdout.write(self.style.SUCCESS('Test users ready!'))
        self.stdout.write(self.style.SUCCESS('Regular user: testuser / testpass123'))
        self.stdout.write(self.style.SUCCESS('Superuser: admin / admin123'))
