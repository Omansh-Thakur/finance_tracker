from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum, Q
from decimal import Decimal
from accounts.models import UserProfile
from accounts.forms import UserProfileForm, UserEditForm
from django.contrib.auth.models import User
from transactions.models import Transaction, Category
from budgets.models import Budget


class DashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard showing financial overview."""
    template_name = 'accounts/dashboard.html'
    login_url = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get all transactions for the user
        transactions = Transaction.objects.filter(user=user)

        # Calculate totals using ORM aggregation
        income_total = transactions.filter(
            category__type='income'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        expense_total = transactions.filter(
            category__type='expense'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        savings = income_total - expense_total

        # Get recent transactions
        recent_transactions = transactions.order_by('-date')[:10]

        # Get budgets and their status
        budgets = Budget.objects.filter(user=user).select_related('category')
        budget_status = []
        for budget in budgets:
            budget_status.append({
                'budget': budget,
                'spent': budget.get_spent_amount(),
                'percentage': budget.get_percentage_used(),
                'exceeded': budget.is_exceeded,
            })

        context.update({
            'total_income': income_total,
            'total_expenses': expense_total,
            'savings': savings,
            'recent_transactions': recent_transactions,
            'budget_status': budget_status,
            'transaction_count': transactions.count(),
        })

        return context


class ProfileView(LoginRequiredMixin, DetailView):
    """View user profile."""
    model = UserProfile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'
    login_url = 'account_login'

    def get_object(self, queryset=None):
        return self.request.user.profile


class EditProfileView(LoginRequiredMixin, UpdateView):
    """Edit user profile."""
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('profile')
    login_url = 'account_login'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)


class EditUserView(LoginRequiredMixin, UpdateView):
    """Edit user information."""
    model = User
    form_class = UserEditForm
    template_name = 'accounts/edit_user.html'
    success_url = reverse_lazy('profile')
    login_url = 'account_login'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'User information updated successfully!')
        return super().form_valid(form)


@login_required(login_url='account_login')
def home_redirect(request):
    """Redirect home to dashboard."""
    return redirect('dashboard')
