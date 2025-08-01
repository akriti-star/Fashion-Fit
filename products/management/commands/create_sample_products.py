from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Product, SizeChart
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample products for testing'

    def handle(self, *args, **options):
        # Get or create a seller user
        seller_user = User.objects.filter(user_type__in=['seller', 'both']).first()
        if not seller_user:
            seller_user = User.objects.filter(is_superuser=True).first()
        
        if not seller_user:
            # Create a test seller
            seller_user = User.objects.create_user(
                username='demoseller',
                email='seller@demo.com',
                password='demo123',
                user_type='seller',
                business_name='Demo Fashion Store',
                is_verified_seller=True
            )
            self.stdout.write(self.style.SUCCESS(f'Created demo seller: {seller_user.username}'))

        # Create sample products
        sample_products = [
            {
                'title': 'Casual T-Shirt',
                'category': 'top',
                'description': 'Comfortable cotton t-shirt perfect for everyday wear',
                'price': Decimal('29.99'),
                'image': 'products/classic_white_tshirt.jpg',
            },
            {
                'title': 'Slim Fit Jeans',
                'category': 'bottom',
                'description': 'Classic blue jeans with a modern slim fit',
                'price': Decimal('79.99'),
                'image': 'products/slim_fit_jeans.jpg',
            },
            {
                'title': 'Summer Dress',
                'category': 'dress',
                'description': 'Light and airy summer dress perfect for warm weather',
                'price': Decimal('59.99'),
                'image': 'products/summer_dress.jpg',
            },
            {
                'title': 'Leather Jacket',
                'category': 'outerwear',
                'description': 'Premium leather jacket for a stylish look',
                'price': Decimal('199.99'),
                'image': 'products/leather_jacket.jpg',
            },
            {
                'title': 'Running Sneakers',
                'category': 'shoes',
                'description': 'Comfortable running shoes for active lifestyle',
                'price': Decimal('89.99'),
                'image': 'products/running_shoes.jpg',
            },
            {
                'title': 'Designer Handbag',
                'category': 'accessories',
                'description': 'Elegant handbag for special occasions',
                'price': Decimal('149.99'),
                'image': 'products/designer_handbag.jpg',
            },
        ]

        created_count = 0
        for product_data in sample_products:
            product, created = Product.objects.get_or_create(
                title=product_data['title'],
                defaults={
                    **product_data,
                    'seller': seller_user,
                    'is_active': True,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created product: {product.title}')
            else:
                # Update existing product with seller
                if not product.seller:
                    product.seller = seller_user
                    product.save()
                    self.stdout.write(f'Updated product with seller: {product.title}')

        # Add size charts if they don't exist
        size_labels = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
        for label in size_labels:
            size_chart, created = SizeChart.objects.get_or_create(
                label=label,
                defaults={
                    'chest_min': 80 + (size_labels.index(label) * 10),
                    'chest_max': 90 + (size_labels.index(label) * 10),
                    'waist_min': 70 + (size_labels.index(label) * 8),
                    'waist_max': 80 + (size_labels.index(label) * 8),
                    'recommended_height': 160 + (size_labels.index(label) * 5),
                }
            )
            if created:
                self.stdout.write(f'Created size chart: {label}')

        self.stdout.write(self.style.SUCCESS(f'Sample products setup complete!'))
        self.stdout.write(self.style.SUCCESS(f'Created {created_count} new products'))
        self.stdout.write(self.style.SUCCESS(f'All products now have sellers assigned'))
