from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('size-guide/', views.SizeGuideView.as_view(), name='size_guide'),
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('try-on/<int:product_id>/', views.try_on_product, name='try_on'),
    path('try-on-test/', views.TryOnTestView.as_view(), name='try_on_test'),
    path('image-test/', views.ImageTestView.as_view(), name='image_test'),
    path('api/virtual-tryon/', views.virtual_tryon_api, name='virtual_tryon_api'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('help/', views.HelpCenterView.as_view(), name='help_center'),
    path('privacy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('terms/', views.TermsOfServiceView.as_view(), name='terms_of_service'),
]
