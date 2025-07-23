from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from products.models import Product


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/create.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, pk=kwargs['product_id'])
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = self.product
        messages.success(self.request, 'Review added successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('products:detail', kwargs={'pk': self.product.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.product
        return context


class ReviewDetailView(DetailView):
    model = Review
    template_name = 'reviews/detail.html'
    context_object_name = 'review'


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/edit.html'
    
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Review updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('products:detail', kwargs={'pk': self.object.product.pk})


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/delete.html'
    
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Review deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('products:detail', kwargs={'pk': self.object.product.pk})


class UserReviewListView(ListView):
    model = Review
    template_name = 'reviews/user_reviews.html'
    context_object_name = 'reviews'
    paginate_by = 10
    
    def get_queryset(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = get_object_or_404(User, pk=self.kwargs['user_id'])
        return Review.objects.filter(user=user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.contrib.auth import get_user_model
        User = get_user_model()
        context['reviewed_user'] = get_object_or_404(User, pk=self.kwargs['user_id'])
        return context
