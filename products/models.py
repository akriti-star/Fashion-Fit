from django.db import models
from django.urls import reverse


class SizeChart(models.Model):
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ]
    
    label = models.CharField(max_length=3, choices=SIZE_CHOICES, unique=True)
    chest_min = models.FloatField(help_text="Minimum chest size in cm")
    chest_max = models.FloatField(help_text="Maximum chest size in cm")
    waist_min = models.FloatField(help_text="Minimum waist size in cm")
    waist_max = models.FloatField(help_text="Maximum waist size in cm")
    recommended_height = models.FloatField(help_text="Recommended height in cm")
    
    def __str__(self):
        return f"Size {self.label}"
    
    class Meta:
        ordering = ['chest_min']


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('top', 'Top'),
        ('bottom', 'Bottom'),
        ('dress', 'Dress'),
        ('outerwear', 'Outerwear'),
        ('shoes', 'Shoes'),
        ('accessories', 'Accessories'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    available_sizes = models.ManyToManyField(SizeChart, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # Add seller field for future functionality
    seller = models.ForeignKey(
        'accounts.CustomUser', 
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
        blank=True,
        help_text="The seller who added this product"
    )
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'pk': self.pk})
    
    def get_average_rating(self):
        reviews = self.review_set.all()
        if not reviews:
            return 0
        total = sum([(r.rating_fit + r.rating_comfort + r.rating_style) / 3 for r in reviews])
        return round(total / len(reviews), 1)
    
    class Meta:
        ordering = ['-created_at']


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=100, blank=True)
    is_primary = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.product.title}"
