from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Force delete all unwanted products'

    def handle(self, *args, **options):
        # Get all products
        all_products = Product.objects.all()
        self.stdout.write(f'Found {all_products.count()} total products')
        
        # Show all products first
        for product in all_products:
            self.stdout.write(f'Product: "{product.title}" (ID: {product.id})')
        
        # Delete products containing these keywords
        keywords = ['sneakers', 'casual', 't shirt', 't-shirt', 'handbag', 'jeans']
        deleted_count = 0
        
        for keyword in keywords:
            products = Product.objects.filter(title__icontains=keyword)
            for product in products:
                self.stdout.write(f'Deleting: "{product.title}"')
                if product.image:
                    try:
                        product.image.delete(save=False)
                    except:
                        pass
                product.delete()
                deleted_count += 1
        
        self.stdout.write(f'Deleted {deleted_count} products')
        
        # Show remaining
        remaining = Product.objects.all()
        self.stdout.write(f'Remaining products: {remaining.count()}')
        for product in remaining:
            self.stdout.write(f'- "{product.title}"')
