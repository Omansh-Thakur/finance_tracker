from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.home_redirect, name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),
    path('user/edit/', views.EditUserView.as_view(), name='edit_user'),
]
