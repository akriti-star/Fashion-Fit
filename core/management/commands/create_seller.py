from django.core.management.base import BaseCommand
from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'Create a seller account for testing'

    def handle(self, *args, **options):
        username = 'testseller'
        email = 'seller@test.com'
        password = 'seller123'
        
        # Check if seller already exists
        if CustomUser.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"Seller account '{username}' already exists!"))
            seller = CustomUser.objects.get(username=username)
        else:
            # Create seller account
            seller = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                user_type='seller',
                first_name='Test',
                last_name='Seller',
                business_name='Test Fashion Store',
                business_address='123 Fashion Street',
                business_phone='555-0123',
                is_verified_seller=True
            )
            self.stdout.write(self.style.SUCCESS(f"Created seller account: {username}"))

        self.stdout.write(f"Seller details:")
        self.stdout.write(f"  Username: {seller.username}")
        self.stdout.write(f"  Email: {seller.email}")
        self.stdout.write(f"  User type: {seller.user_type}")
        self.stdout.write(f"  Is seller: {seller.is_seller()}")
        self.stdout.write(f"  Can sell: {seller.can_sell()}")
        self.stdout.write(f"  Is verified: {seller.is_verified_seller}")
        self.stdout.write(f"\nYou can now login as: {username} / {password}")
