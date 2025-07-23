from django.urls import path
from . import views

app_name = 'outfits'

urlpatterns = [
    path('', views.OutfitListView.as_view(), name='list'),
    path('create/', views.OutfitCreateView.as_view(), name='create'),
    path('<int:pk>/', views.OutfitDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.OutfitUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.OutfitDeleteView.as_view(), name='delete'),
    path('<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('builder/', views.OutfitBuilderView.as_view(), name='builder'),
]
