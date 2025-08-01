from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from outfits.models import Outfit
from products.models import Product
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample outfits for the trending outfits section'

    def handle(self, *args, **options):
        # Get or create users
        users = []
        for i in range(3):
            user, created = User.objects.get_or_create(
                username=f'outfit_user_{i+1}',
                defaults={
                    'email': f'user{i+1}@example.com',
                    'user_type': 'buyer',
                    'first_name': f'User{i+1}',
                    'last_name': 'Fashion',
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {user.username}')
            users.append(user)

        # Get all products
        products = list(Product.objects.all())
        if not products:
            self.stdout.write(self.style.ERROR('No products found! Run create_sample_products first.'))
            return

        # Sample outfit data
        outfits_data = [
            {
                'name': 'Casual Weekend Look',
                'description': 'Perfect for a relaxed weekend outing with friends.',
                'product_count': 3,
                'is_public': True,
            },
            {
                'name': 'Business Professional',
                'description': 'Elegant and professional outfit for the workplace.',
                'product_count': 2,
                'is_public': True,
            },
            {
                'name': 'Summer Chic',
                'description': 'Light and stylish outfit for sunny days.',
                'product_count': 3,
                'is_public': True,
            },
            {
                'name': 'Evening Elegance',
                'description': 'Sophisticated look for special occasions.',
                'product_count': 2,
                'is_public': True,
            },
            {
                'name': 'Sporty Casual',
                'description': 'Comfortable and trendy for active lifestyle.',
                'product_count': 3,
                'is_public': True,
            },
        ]

        created_count = 0
        for outfit_data in outfits_data:
            # Check if outfit already exists
            if Outfit.objects.filter(name=outfit_data['name']).exists():
                self.stdout.write(f'Outfit already exists: {outfit_data["name"]}')
                continue

            # Create outfit
            outfit = Outfit.objects.create(
                name=outfit_data['name'],
                description=outfit_data['description'],
                user=random.choice(users),
                is_public=outfit_data['is_public']
            )

            # Add random products to outfit
            selected_products = random.sample(products, min(outfit_data['product_count'], len(products)))
            outfit.products.set(selected_products)

            created_count += 1
            self.stdout.write(f'Created outfit: {outfit.name} (${outfit.get_total_price():.2f})')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} sample outfits')
        )
        
        # Display all outfits
        all_outfits = Outfit.objects.all()
        self.stdout.write(f'\nTotal outfits in system: {all_outfits.count()}')
        for outfit in all_outfits:
            self.stdout.write(f'- {outfit.name} by {outfit.user.username} (${outfit.get_total_price():.2f})')
