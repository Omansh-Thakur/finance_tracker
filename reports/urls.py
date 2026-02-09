from django.urls import path
from reports import views

urlpatterns = [
    path('monthly/', views.MonthlyReportView.as_view(), name='monthly_report'),
    path('categories/', views.CategoryReportView.as_view(), name='category_report'),
]
