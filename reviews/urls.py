from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('product/<int:product_id>/create/', views.ReviewCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ReviewDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ReviewUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='delete'),
    path('user/<int:user_id>/', views.UserReviewListView.as_view(), name='user_reviews'),
]
