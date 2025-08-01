from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Update summer dress to use latest uploaded image'

    def handle(self, *args, **options):
        try:
            product = Product.objects.get(title='Summer Dress')
            old_image = product.image
            
            # Update to use the latest image with unique name
            product.image = 'products/summer_dress_latest.jpg'
            product.save()
            
            self.stdout.write(f'Updated Summer Dress image from: {old_image}')
            self.stdout.write(f'Updated Summer Dress image to: {product.image}')
            self.stdout.write(self.style.SUCCESS('Successfully updated to latest image!'))
            
        except Product.DoesNotExist:
            self.stdout.write(self.style.ERROR('Summer Dress product not found'))
