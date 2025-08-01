from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils.deprecation import MiddlewareMixin


class AdminAccessMiddleware(MiddlewareMixin):
    """
    Middleware to restrict admin access to superusers only.
    """
    
    def process_request(self, request):
        # Check if the request is for admin URLs
        if request.path.startswith('/admin/'):
            # Allow access to admin login page
            if request.path == '/admin/login/' or request.path == '/admin/login':
                return None
            
            # Check if user is authenticated
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('accounts:login'))
            
            # Check if user is superuser
            if not request.user.is_superuser:
                messages.error(request, 'You do not have permission to access the admin panel.')
                return HttpResponseRedirect(reverse('core:home'))
        
        return None
