from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from .models import Outfit, OutfitLike
from .forms import OutfitForm, OutfitBuilderForm
from products.models import Product


class OutfitListView(ListView):
    model = Outfit
    template_name = 'outfits/list.html'
    context_object_name = 'outfits'
    paginate_by = 12
    
    def get_queryset(self):
        return Outfit.objects.filter(is_public=True)


class OutfitDetailView(DetailView):
    model = Outfit
    template_name = 'outfits/detail.html'
    context_object_name = 'outfit'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        outfit = self.get_object()
        context['total_price'] = outfit.get_total_price()
        
        if self.request.user.is_authenticated:
            context['user_liked'] = OutfitLike.objects.filter(
                user=self.request.user, outfit=outfit
            ).exists()
        
        return context


class OutfitCreateView(LoginRequiredMixin, CreateView):
    model = Outfit
    form_class = OutfitForm
    template_name = 'outfits/create.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Outfit created successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('outfits:detail', kwargs={'pk': self.object.pk})


class OutfitUpdateView(LoginRequiredMixin, UpdateView):
    model = Outfit
    form_class = OutfitForm
    template_name = 'outfits/edit.html'
    
    def get_queryset(self):
        return Outfit.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Outfit updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('outfits:detail', kwargs={'pk': self.object.pk})


class OutfitDeleteView(LoginRequiredMixin, DeleteView):
    model = Outfit
    template_name = 'outfits/delete.html'
    success_url = reverse_lazy('outfits:list')
    
    def get_queryset(self):
        return Outfit.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Outfit deleted successfully!')
        return super().delete(request, *args, **kwargs)


@login_required
def toggle_like(request, pk):
    outfit = get_object_or_404(Outfit, pk=pk)
    
    like, created = OutfitLike.objects.get_or_create(
        user=request.user, outfit=outfit
    )
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    return JsonResponse({'liked': liked})


class OutfitBuilderView(LoginRequiredMixin, TemplateView):
    template_name = 'outfits/builder.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(is_active=True)
        context['categories'] = Product.CATEGORY_CHOICES
        return context
    
    def post(self, request):
        name = request.POST.get('outfit_name')
        selected_products = request.POST.getlist('products')
        is_public = request.POST.get('is_public') == 'on'
        
        if name and selected_products:
            outfit = Outfit.objects.create(
                user=request.user,
                name=name,
                is_public=is_public
            )
            
            products = Product.objects.filter(id__in=selected_products)
            outfit.products.set(products)
            
            messages.success(request, 'Outfit created successfully!')
            return redirect('outfits:detail', pk=outfit.pk)
        
        messages.error(request, 'Please provide an outfit name and select at least one product.')
        return redirect('outfits:builder')
