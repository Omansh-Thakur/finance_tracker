from django.urls import path
from transactions import views

urlpatterns = [
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/new/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),

    # Transactions
    path('', views.TransactionListView.as_view(), name='transaction_list'),
    path('<int:pk>/', views.TransactionDetailView.as_view(), name='transaction_detail'),
    path('new/', views.TransactionCreateView.as_view(), name='transaction_create'),
    path('<int:pk>/edit/', views.TransactionUpdateView.as_view(), name='transaction_update'),
    path('<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='transaction_delete'),
]
