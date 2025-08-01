from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.urls import reverse_lazy
from .models import Product, SizeChart
from .forms import ProductForm
from core.models import Wishlist, TryOnSession
from reviews.models import Review


class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        category = self.kwargs.get('category')
        queryset = Product.objects.filter(is_active=True)
        if category:
            queryset = queryset.filter(category=category)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs.get('category')
        context['categories'] = Product.CATEGORY_CHOICES
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['reviews'] = Review.objects.filter(product=product)
        context['average_rating'] = product.get_average_rating()
        context['size_charts'] = product.available_sizes.all()
        
        if self.request.user.is_authenticated:
            context['recommended_size'] = self.request.user.get_recommended_size()
            context['in_wishlist'] = Wishlist.objects.filter(
                user=self.request.user, product=product
            ).exists()
        
        return context


class ProductCategoryView(ListView):
    model = Product
    template_name = 'products/category.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        category = self.kwargs['category']
        return Product.objects.filter(category=category, is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs['category']
        return context


class ProductSearchView(ListView):
    model = Product
    template_name = 'products/search.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Product.objects.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) | 
                Q(category__icontains=query),
                is_active=True
            )
        return Product.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class TryOnView(LoginRequiredMixin, TemplateView):
    template_name = 'products/try_on.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        context['product'] = product
        
        # Create try-on session
        TryOnSession.objects.create(user=self.request.user, product=product)
        
        return context


@login_required
def size_recommendation(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    
    recommended_size = user.get_recommended_size()
    
    data = {
        'recommended_size': recommended_size,
        'user_measurements': {
            'height': user.height_cm,
            'weight': user.weight_kg,
            'chest': user.chest_cm,
            'waist': user.waist_cm,
            'hips': user.hips_cm,
            'body_type': user.body_type,
        },
        'product_title': product.title,
        'product_category': product.category,
    }
    
    return JsonResponse(data)


class AddToWishlistView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user, product=product
        )
        
        if created:
            messages.success(request, f'{product.title} added to wishlist!')
        else:
            wishlist_item.delete()
            messages.info(request, f'{product.title} removed from wishlist!')
        
        return redirect(request.META.get('HTTP_REFERER', 'products:list'))


# ==================== SELLER PRODUCT MANAGEMENT ====================

class SellerProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/seller/list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_seller():
            messages.error(request, 'Access denied. Seller account required.')
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)


class SellerProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/seller/create.html'
    success_url = reverse_lazy('products:seller_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['seller'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, 'Product created successfully!')
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_seller():
            messages.error(request, 'Access denied. Seller account required.')
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)


class SellerProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/seller/update.html'
    success_url = reverse_lazy('products:seller_list')
    
    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['seller'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, 'Product updated successfully!')
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_seller():
            messages.error(request, 'Access denied. Seller account required.')
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)


class SellerProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/seller/delete.html'
    success_url = reverse_lazy('products:seller_list')
    
    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Product deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_seller():
            messages.error(request, 'Access denied. Seller account required.')
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)
        return redirect('products:detail', pk=pk)
