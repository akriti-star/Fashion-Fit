from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied


class BaseUserMixin(LoginRequiredMixin):
    """Base mixin for all user-related views"""
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = self.request.user.user_type
        context['is_buyer'] = self.request.user.is_buyer()
        context['is_seller'] = self.request.user.is_seller()
        return context


class BuyerRequiredMixin(BaseUserMixin, UserPassesTestMixin):
    """Mixin to ensure only buyers can access the view"""
    
    def test_func(self):
        return self.request.user.is_buyer()
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, "You need buyer privileges to access this page.")
            return redirect('accounts:dashboard_selector')
        return super().handle_no_permission()


class SellerRequiredMixin(BaseUserMixin, UserPassesTestMixin):
    """Mixin to ensure only sellers can access the view"""
    
    def test_func(self):
        return self.request.user.is_seller()
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, "You need seller privileges to access this page.")
            return redirect('accounts:dashboard_selector')
        return super().handle_no_permission()


class VerifiedSellerRequiredMixin(SellerRequiredMixin):
    """Mixin to ensure only verified sellers can access the view"""
    
    def test_func(self):
        return self.request.user.can_sell()
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            if not self.request.user.is_seller():
                messages.error(self.request, "You need seller privileges to access this page.")
            else:
                messages.error(self.request, "You need to be a verified seller to access this page.")
            return redirect('accounts:dashboard_selector')
        return super().handle_no_permission()


# Abstract Base Views for Buyers
class BuyerDashboardView(BuyerRequiredMixin, TemplateView):
    """Abstract dashboard view for buyers"""
    template_name = 'accounts/buyer/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add buyer-specific context
        context['recent_orders'] = self.get_recent_orders()
        context['wishlist_count'] = self.get_wishlist_count()
        context['recommended_products'] = self.get_recommended_products()
        return context
    
    def get_recent_orders(self):
        """Override in subclass to implement order logic"""
        return []
    
    def get_wishlist_count(self):
        """Override in subclass to implement wishlist logic"""
        return 0
    
    def get_recommended_products(self):
        """Override in subclass to implement recommendation logic"""
        return []


class BuyerProfileView(BuyerRequiredMixin, TemplateView):
    """Abstract profile view for buyers"""
    template_name = 'accounts/buyer/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.request.user
        context['recommended_size'] = self.request.user.get_recommended_size()
        return context


# Abstract Base Views for Sellers
class SellerDashboardView(SellerRequiredMixin, TemplateView):
    """Abstract dashboard view for sellers"""
    template_name = 'accounts/seller/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add seller-specific context
        context['total_products'] = self.get_total_products()
        context['total_orders'] = self.get_total_orders()
        context['total_revenue'] = self.get_total_revenue()
        context['pending_orders'] = self.get_pending_orders()
        return context
    
    def get_total_products(self):
        """Override in subclass to implement product counting"""
        return 0
    
    def get_total_orders(self):
        """Override in subclass to implement order counting"""
        return 0
    
    def get_total_revenue(self):
        """Override in subclass to implement revenue calculation"""
        return 0
    
    def get_pending_orders(self):
        """Override in subclass to implement pending orders"""
        return []


class SellerProfileView(SellerRequiredMixin, TemplateView):
    """Abstract profile view for sellers"""
    template_name = 'accounts/seller/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seller_profile'] = self.request.user
        context['business_info'] = {
            'name': self.request.user.business_name,
            'description': self.request.user.business_description,
            'verified': self.request.user.is_verified_seller,
        }
        return context


class SellerProductListView(VerifiedSellerRequiredMixin, ListView):
    """Abstract product list view for sellers"""
    template_name = 'accounts/seller/products.html'
    context_object_name = 'products'
    paginate_by = 10
    
    def get_queryset(self):
        """Override in subclass to implement product filtering"""
        return []


class DashboardSelectorView(BaseUserMixin, TemplateView):
    """View to select appropriate dashboard based on user type"""
    template_name = 'accounts/dashboard_selector.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.user_type == 'buyer':
            return redirect('accounts:buyer_dashboard')
        elif request.user.user_type == 'seller':
            return redirect('accounts:seller_dashboard')
        else:  # both
            return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_access_buyer'] = self.request.user.is_buyer()
        context['can_access_seller'] = self.request.user.is_seller()
        return context
