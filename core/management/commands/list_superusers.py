from django.core.management.base import BaseCommand
from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'List all superusers and their details'

    def handle(self, *args, **options):
        superusers = CustomUser.objects.filter(is_superuser=True)
        
        if not superusers.exists():
            self.stdout.write(self.style.WARNING('No superusers found in the database.'))
            self.stdout.write(self.style.SUCCESS('To create a superuser, run: python manage.py createsuperuser'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Found {superusers.count()} superuser(s):'))
        self.stdout.write('-' * 60)
        
        for user in superusers:
            self.stdout.write(f'Username: {user.username}')
            self.stdout.write(f'Email: {user.email}')
            self.stdout.write(f'First Name: {user.first_name or "Not set"}')
            self.stdout.write(f'Last Name: {user.last_name or "Not set"}')
            self.stdout.write(f'User Type: {user.user_type}')
            self.stdout.write(f'Is Active: {user.is_active}')
            self.stdout.write(f'Is Staff: {user.is_staff}')
            self.stdout.write(f'Is Superuser: {user.is_superuser}')
            self.stdout.write(f'Date Joined: {user.date_joined}')
            self.stdout.write(f'Last Login: {user.last_login or "Never"}')
            
            if user.user_type == 'seller':
                self.stdout.write(f'Business Name: {user.business_name or "Not set"}')
                self.stdout.write(f'Is Verified Seller: {user.is_verified_seller}')
            
            self.stdout.write('-' * 60)
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Note: Passwords are hashed and cannot be displayed.'))
        self.stdout.write(self.style.SUCCESS('To reset a password, use: python manage.py changepassword <username>'))
        self.stdout.write(self.style.SUCCESS('To access admin panel, go to: http://127.0.0.1:8000/admin/'))
