from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from .forms import CustomUserCreationForm, ProfileUpdateForm, CustomLoginForm
from .models import CustomUser, UserProfile
from products.models import Product
from .base_views import (
    BuyerDashboardView, BuyerProfileView, 
    SellerDashboardView, SellerProfileView, SellerProductListView,
    DashboardSelectorView
)
from products.models import Product
from outfits.models import Outfit


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """Redirect user based on their profile type"""
        user = self.request.user
        
        # Set session preference based on user type
        self.request.session['login_as'] = user.user_type
        
        # Redirect based on user type
        if user.user_type == 'buyer':
            return reverse_lazy('accounts:buyer_dashboard')
        elif user.user_type == 'seller':
            return reverse_lazy('accounts:seller_dashboard')
        else:  # both
            return reverse_lazy('accounts:dashboard')
    
    def form_valid(self, form):
        """Handle successful login"""
        user = form.get_user()
        
        # Add success message based on user type
        if user.user_type == 'buyer':
            messages.success(self.request, f'Welcome back, {user.get_full_name() or user.username}! Logged in as buyer.')
        elif user.user_type == 'seller':
            messages.success(self.request, f'Welcome back, {user.get_full_name() or user.username}! Logged in as seller.')
        else:  # both
            messages.success(self.request, f'Welcome back, {user.get_full_name() or user.username}!')
        
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """Custom logout view that always redirects to home page"""
    next_page = reverse_lazy('core:home')
    
    def dispatch(self, request, *args, **kwargs):
        # Add success message before logout
        if request.user.is_authenticated:
            if request.user.is_superuser:
                messages.success(request, 'Admin logout successful!')
            else:
                messages.success(request, 'You have been logged out successfully!')
        
        # Call the parent dispatch to handle the logout
        return super().dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    
    def form_valid(self, form):
        # Save the user
        user = form.save()
        
        # Login the user automatically
        login(self.request, user)
        
        # Set session preference based on user type
        self.request.session['login_as'] = user.user_type
        
        # Add success message based on user type
        if user.user_type == 'buyer':
            messages.success(self.request, f'Welcome to FashionFit, {user.get_full_name()}! Your buyer profile has been created successfully.')
        elif user.user_type == 'seller':
            messages.success(self.request, f'Welcome to FashionFit, {user.get_full_name()}! Your seller profile has been created successfully.')
        else:  # both
            messages.success(self.request, f'Welcome to FashionFit, {user.get_full_name()}! Your profile has been created with both buyer and seller capabilities.')
        
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect user based on their profile type"""
        user = self.object
        if user.user_type == 'buyer':
            return reverse_lazy('accounts:buyer_dashboard')
        elif user.user_type == 'seller':
            return reverse_lazy('accounts:seller_dashboard')
        else:  # both
            return reverse_lazy('accounts:dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Account created successfully!')
        return response


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/profile.html'
    context_object_name = 'user_profile'
    
    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)


class MeasurementsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/measurements.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_measurements'] = {
            'height': self.request.user.height_cm,
            'weight': self.request.user.weight_kg,
            'chest': self.request.user.chest_cm,
            'waist': self.request.user.waist_cm,
            'hips': self.request.user.hips_cm,
            'body_type': self.request.user.body_type,
        }
        return context


class SizeRecommendationView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/size_recommendation.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recommended_size'] = self.request.user.get_recommended_size()
        return context


# Concrete Buyer Views
class ConcreteBuyerDashboardView(BuyerDashboardView):
    """Concrete buyer dashboard with actual implementation"""
    
    def get_recent_orders(self):
        # Implementation for recent orders
        # This would typically fetch from an Order model
        return []
    
    def get_wishlist_count(self):
        # Implementation for wishlist count
        # This would typically count items in user's wishlist
        return 0
    
    def get_recommended_products(self):
        # Implementation for product recommendations
        return Product.objects.filter(is_active=True)[:6]


class ConcreteBuyerProfileView(BuyerProfileView):
    """Concrete buyer profile view"""
    pass


# Concrete Seller Views
class ConcreteSellerDashboardView(SellerDashboardView):
    """Concrete seller dashboard with actual implementation"""
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add recent products
        context['recent_products'] = Product.objects.filter(seller=self.request.user).order_by('-created_at')[:5]
        # Add product categories count
        from django.db.models import Count
        context['product_categories'] = Product.objects.filter(seller=self.request.user).values('category').annotate(count=Count('category')).order_by('-count')
        return context
    
    def get_total_products(self):
        # Count products added by this seller
        return Product.objects.filter(seller=self.request.user).count()
    
    def get_total_orders(self):
        # Count orders for this seller's products
        # This would typically query an Order model
        return 0
    
    def get_total_revenue(self):
        # Calculate total revenue for this seller
        return 0
        # This would typically sum order amounts
        return 0
    
    def get_pending_orders(self):
        # Get pending orders for this seller
        return []


class ConcreteSellerProfileView(SellerProfileView):
    """Concrete seller profile view"""
    pass


class ConcreteSellerProductListView(SellerProductListView):
    """Concrete seller product list view"""
    
    def get_queryset(self):
        # Return products belonging to the current seller
        return Product.objects.filter(seller=self.request.user)


# Dashboard Selector
class ConcreteDashboardSelectorView(DashboardSelectorView):
    """Concrete dashboard selector"""
    pass


@login_required
def dashboard_selector(request):
    """Function-based dashboard selector for users with multiple roles"""
    context = {
        'can_access_buyer': request.user.is_buyer(),
        'can_access_seller': request.user.is_seller(),
    }
    return render(request, 'accounts/dashboard_selector.html', context)
