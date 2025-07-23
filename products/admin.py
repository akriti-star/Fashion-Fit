from django.contrib import admin
from .models import Product, SizeChart, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    filter_horizontal = ['available_sizes']
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'category', 'description', 'price', 'image', 'is_active')
        }),
        ('Size Information', {
            'fields': ('available_sizes',)
        }),
    )


class SizeChartAdmin(admin.ModelAdmin):
    list_display = ['label', 'chest_min', 'chest_max', 'waist_min', 'waist_max', 'recommended_height']
    list_filter = ['label']
    ordering = ['chest_min']


admin.site.register(Product, ProductAdmin)
admin.site.register(SizeChart, SizeChartAdmin)
admin.site.register(ProductImage)
