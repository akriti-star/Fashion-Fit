from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import UserProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'Create test users for buyer/seller functionality'

    def handle(self, *args, **options):
        # Create test buyer
        buyer, created = User.objects.get_or_create(
            username='testbuyer',
            defaults={
                'email': 'buyer@test.com',
                'first_name': 'Test',
                'last_name': 'Buyer',
                'user_type': 'buyer',
            }
        )
        if created:
            buyer.set_password('testpass123')
            buyer.save()
            self.stdout.write(self.style.SUCCESS('Created test buyer: testbuyer/testpass123'))
        else:
            self.stdout.write(self.style.WARNING('Test buyer already exists'))

        # Create test seller
        seller, created = User.objects.get_or_create(
            username='testseller',
            defaults={
                'email': 'seller@test.com',
                'first_name': 'Test',
                'last_name': 'Seller',
                'user_type': 'seller',
                'business_name': 'Test Fashion Store',
                'business_description': 'A test fashion store for demonstration',
                'is_verified_seller': True,
            }
        )
        if created:
            seller.set_password('testpass123')
            seller.save()
            self.stdout.write(self.style.SUCCESS('Created test seller: testseller/testpass123'))
        else:
            self.stdout.write(self.style.WARNING('Test seller already exists'))

        # Create test user with both roles
        both_user, created = User.objects.get_or_create(
            username='testboth',
            defaults={
                'email': 'both@test.com',
                'first_name': 'Test',
                'last_name': 'Both',
                'user_type': 'both',
                'business_name': 'Test Multi Store',
                'business_description': 'A test store with both buyer and seller capabilities',
                'is_verified_seller': True,
            }
        )
        if created:
            both_user.set_password('testpass123')
            both_user.save()
            self.stdout.write(self.style.SUCCESS('Created test both user: testboth/testpass123'))
        else:
            self.stdout.write(self.style.WARNING('Test both user already exists'))

        self.stdout.write(self.style.SUCCESS('Test users setup complete!'))
        self.stdout.write(self.style.SUCCESS('You can now test the login functionality with:'))
        self.stdout.write(self.style.SUCCESS('- Buyer: testbuyer/testpass123'))
        self.stdout.write(self.style.SUCCESS('- Seller: testseller/testpass123'))
        self.stdout.write(self.style.SUCCESS('- Both: testboth/testpass123'))
