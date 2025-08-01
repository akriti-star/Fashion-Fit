# from django.core.management.base import BaseCommand
# from products.models import Product


# class Command(BaseCommand):
#     help = 'Update image paths for existing products'

#     def handle(self, *args, **options):
#         # Mapping of product titles to correct image paths
#         # image_updates = {
#         #     'Casual T-Shirt': 'products/classic_white_tshirt.jpg',
#         #     'Slim Fit Jeans': 'products/slim_fit_jeans.jpg',
#         #     'Summer Dress': 'products/summer_dress.jpg',
#         #     'Leather Jacket': 'products/leather_jacket.jpg',
#         #     'Running Sneakers': 'products/running_shoes.jpg',
#         #     'Designer Handbag': 'products/designer_handbag.jpg',
#         # }

#         updated_count = 0
#         for title, image_path in image_updates.items():
#             try:
#                 product = Product.objects.get(title=title)
#                 product.image = image_path
#                 product.save()
#                 updated_count += 1
#                 self.stdout.write(f'Updated {title} with image: {image_path}')
#             except Product.DoesNotExist:
#                 self.stdout.write(f'Product "{title}" not found, skipping...')

#         self.stdout.write(self.style.SUCCESS(f'Updated {updated_count} products with correct image paths'))
