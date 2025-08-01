from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Update leather jacket to latest uploaded image'

    def handle(self, *args, **options):
        try:
            product = Product.objects.get(title='Leather Jacket')
            old_image = product.image
            
            # Update to use the latest image with unique name
            product.image = 'products/leather_jacket_latest.jpg'
            product.save()
            
            self.stdout.write(f'Updated Leather Jacket image from: {old_image}')
            self.stdout.write(f'Updated Leather Jacket image to: {product.image}')
            self.stdout.write(self.style.SUCCESS('Successfully updated Leather Jacket to latest image!'))
            
        except Product.DoesNotExist:
            self.stdout.write(self.style.ERROR('Leather Jacket product not found'))
