from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('measurements/', views.MeasurementsView.as_view(), name='measurements'),
    path('size-recommendation/', views.SizeRecommendationView.as_view(), name='size_recommendation'),
    
    # Dashboard routing
    path('dashboard/', views.dashboard_selector, name='dashboard'),
    path('dashboard/buyer/', views.ConcreteBuyerDashboardView.as_view(), name='buyer_dashboard'),
    path('dashboard/seller/', views.ConcreteSellerDashboardView.as_view(), name='seller_dashboard'),
    
    # Profile routing
    path('profile/buyer/', views.ConcreteBuyerProfileView.as_view(), name='buyer_profile'),
    path('profile/seller/', views.ConcreteSellerProfileView.as_view(), name='seller_profile'),
    
    # Seller-specific URLs
    path('seller/products/', views.ConcreteSellerProductListView.as_view(), name='seller_products'),
]
