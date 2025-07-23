from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Delete specific products by name'

    def handle(self, *args, **options):
        products_to_delete = [
            'running sneakers',
            'Running Sneakers',
            'Casual T Shirt',
            'casual t shirt', 
            'Designer handbag',
            'designer handbag',
            'Slim fit jeans',
            'slim fit jeans',
            'Sneakers',
            'T-Shirt',
            'Handbag',
            'Jeans'
        ]
        
        deleted_count = 0
        
        # First, let's see all products in the database
        all_products = Product.objects.all()
        self.stdout.write(f'Total products in database: {all_products.count()}')
        
        if all_products.exists():
            self.stdout.write('Current products:')
            for product in all_products:
                self.stdout.write(f'- "{product.title}" (ID: {product.id})')
        
        self.stdout.write('')
        self.stdout.write('Starting deletion process...')
        
        for product_name in products_to_delete:
            # Try exact match first
            products = Product.objects.filter(title__iexact=product_name)
            
            if not products.exists():
                # Try partial match if exact doesn't work
                products = Product.objects.filter(title__icontains=product_name)
            
            if products.exists():
                for product in products:
                    self.stdout.write(f'Deleting product: "{product.title}" (ID: {product.id})')
                    # Delete associated image file if it exists
                    if product.image:
                        try:
                            product.image.delete(save=False)
                            self.stdout.write(f'  - Deleted image: {product.image.name}')
                        except Exception as e:
                            self.stdout.write(f'  - Could not delete image: {e}')
                    product.delete()
                    deleted_count += 1
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {deleted_count} product(s)'))
        
        # Show remaining products
        remaining_products = Product.objects.all()
        if remaining_products.exists():
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS(f'Remaining products ({remaining_products.count()}):'))
            for product in remaining_products:
                self.stdout.write(f'- "{product.title}" (by {product.seller.username if product.seller else "Unknown"})')
        else:
            self.stdout.write(self.style.WARNING('No products remaining in database'))
