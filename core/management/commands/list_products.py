from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'List all products in the database'

    def handle(self, *args, **options):
        products = Product.objects.all()
        
        if not products.exists():
            self.stdout.write(self.style.WARNING('No products found in the database.'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Found {products.count()} product(s):'))
        self.stdout.write('-' * 60)
        
        for product in products:
            self.stdout.write(f'Title: {product.title}')
            self.stdout.write(f'Category: {product.category}')
            self.stdout.write(f'Price: ${product.price}')
            self.stdout.write(f'Seller: {product.seller.username if product.seller else "No seller"}')
            self.stdout.write(f'Image: {product.image.name if product.image else "No image"}')
            self.stdout.write('-' * 60)
