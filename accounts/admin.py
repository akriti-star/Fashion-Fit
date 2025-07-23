from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'height_cm', 'weight_kg', 'body_type', 'gender']
    fieldsets = UserAdmin.fieldsets + (
        ('Body Measurements', {
            'fields': ('height_cm', 'weight_kg', 'body_type', 'gender', 'chest_cm', 'waist_cm', 'hips_cm')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Body Measurements', {
            'fields': ('height_cm', 'weight_kg', 'body_type', 'gender', 'chest_cm', 'waist_cm', 'hips_cm')
        }),
    )


# Custom admin site class to restrict access to superusers only
class CustomAdminSite(admin.AdminSite):
    site_header = 'FashionFit Admin'
    site_title = 'FashionFit Admin'
    index_title = 'Welcome to FashionFit Administration'
    
    def has_permission(self, request):
        """
        Only allow superusers to access the admin site.
        """
        return request.user.is_active and request.user.is_superuser
    
    def admin_view(self, view, cacheable=False):
        """
        Override admin_view to check superuser status and redirect non-superusers.
        """
        def inner(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('accounts:login'))
            if not request.user.is_superuser:
                messages.error(request, 'You do not have permission to access the admin panel.')
                return HttpResponseRedirect(reverse('core:home'))
            return view(request, *args, **kwargs)
        return inner


# Override default admin site behavior
class RestrictedAdminSite(admin.AdminSite):
    def has_permission(self, request):
        """
        Override to only allow superusers.
        """
        return request.user.is_active and request.user.is_superuser


# Replace the default admin site
admin.site.__class__ = RestrictedAdminSite

admin.site.register(CustomUser, CustomUserAdmin)
