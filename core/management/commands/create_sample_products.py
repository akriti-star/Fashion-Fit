from django.core.management.base import BaseCommand
from products.models import Product
from accounts.models import CustomUser
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class Command(BaseCommand):
    help = 'Create sample products for testing'

    def handle(self, *args, **options):
        # Get or create a seller account
        seller, created = CustomUser.objects.get_or_create(
            username='sample_seller',
            defaults={
                'email': 'seller@example.com',
                'user_type': 'seller',
                'first_name': 'Sample',
                'last_name': 'Seller',
                'business_name': 'Sample Fashion Store',
                'business_address': '123 Fashion St',
                'business_phone': '555-0123'
            }
        )
        
        if created:
            seller.set_password('seller123')
            seller.save()
            self.stdout.write(f'Created seller account: {seller.username}')
        else:
            self.stdout.write(f'Using existing seller account: {seller.username}')

        # Sample products data
        products_data = [
            {
                'title': 'Classic White T-Shirt',
                'category': 'top',
                'description': 'A comfortable classic white t-shirt perfect for everyday wear.',
                'price': 29.99,
            },
            {
                'title': 'Blue Denim Jeans',
                'category': 'bottom',
                'description': 'Comfortable slim-fit denim jeans in classic blue.',
                'price': 79.99,
            },
            {
                'title': 'Summer Floral Dress',
                'category': 'dress',
                'description': 'Beautiful floral dress perfect for summer occasions.',
                'price': 89.99,
            },
            {
                'title': 'Black Leather Jacket',
                'category': 'outerwear',
                'description': 'Stylish black leather jacket for a cool look.',
                'price': 199.99,
            },
            {
                'title': 'Running Sneakers',
                'category': 'shoes',
                'description': 'Comfortable running sneakers for active lifestyle.',
                'price': 129.99,
            },
            {
                'title': 'Designer Handbag',
                'category': 'accessories',
                'description': 'Elegant designer handbag for special occasions.',
                'price': 249.99,
            },
        ]

        created_count = 0
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                title=product_data['title'],
                defaults={
                    'category': product_data['category'],
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'seller': seller,
                    'is_active': True,
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'Created product: {product.title}')
            else:
                self.stdout.write(f'Product already exists: {product.title}')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} products')
        )
        self.stdout.write(
            self.style.SUCCESS('You can now select these products when creating/editing outfits!')
        )
        self.stdout.write(
            self.style.SUCCESS('Login as a seller to add more products at /products/seller/')
        )
