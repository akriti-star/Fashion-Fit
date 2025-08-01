from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    path('category/<str:category>/', views.ProductListView.as_view(), name='category'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='detail'),
    path('size-recommendation/<int:product_id>/', views.size_recommendation, name='size_recommendation'),
    path('search/', views.ProductSearchView.as_view(), name='search'),
    
    # Seller product management URLs
    path('seller/', views.SellerProductListView.as_view(), name='seller_list'),
    path('seller/create/', views.SellerProductCreateView.as_view(), name='seller_create'),
    path('seller/<int:pk>/update/', views.SellerProductUpdateView.as_view(), name='seller_update'),
    path('seller/<int:pk>/delete/', views.SellerProductDeleteView.as_view(), name='seller_delete'),
]
