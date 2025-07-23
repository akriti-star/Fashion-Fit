from django.contrib import admin
from .models import Wishlist, TryOnSession, Contact


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__title']


class TryOnSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__title']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'inquiry_type', 'subject', 'status', 'created_at']
    list_filter = ['inquiry_type', 'status', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message Details', {
            'fields': ('inquiry_type', 'subject', 'message')
        }),
        ('Status & Timestamps', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )


admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(TryOnSession, TryOnSessionAdmin)
