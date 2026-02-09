from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from budgets.models import Budget
from budgets.forms import BudgetForm


class BudgetListView(LoginRequiredMixin, ListView):
    """List all budgets for the user."""
    model = Budget
    template_name = 'budgets/budget_list.html'
    context_object_name = 'budgets'
    paginate_by = 20
    login_url = 'account_login'

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        budgets = self.get_queryset()

        # Add budget status information
        budget_status = []
        for budget in budgets:
            budget_status.append({
                'budget': budget,
                'spent': budget.get_spent_amount(),
                'percentage': budget.get_percentage_used(),
                'exceeded': budget.is_exceeded,
                'remaining': budget.monthly_limit - budget.get_spent_amount(),
            })

        context['budget_status'] = budget_status
        context['total_budgets'] = len(budget_status)

        # Count exceeded budgets
        exceeded_count = sum(1 for b in budget_status if b['exceeded'])
        context['exceeded_count'] = exceeded_count

        return context


class BudgetDetailView(LoginRequiredMixin, DetailView):
    """View budget details."""
    model = Budget
    template_name = 'budgets/budget_detail.html'
    context_object_name = 'budget'
    login_url = 'account_login'

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        budget = self.get_object()

        context['spent'] = budget.get_spent_amount()
        context['percentage'] = budget.get_percentage_used()
        context['exceeded'] = budget.is_exceeded
        context['remaining'] = budget.monthly_limit - context['spent']

        # Get transactions for this category this month
        from django.utils import timezone
        from transactions.models import Transaction

        today = timezone.now().date()
        current_month_start = today.replace(day=1)

        if today.month == 12:
            current_month_end = today.replace(year=today.year + 1, month=1, day=1)
        else:
            current_month_end = today.replace(month=today.month + 1, day=1)

        context['recent_transactions'] = Transaction.objects.filter(
            category=budget.category,
            user=self.request.user,
            date__gte=current_month_start,
            date__lt=current_month_end,
        ).order_by('-date')[:10]

        return context


class BudgetCreateView(LoginRequiredMixin, CreateView):
    """Create a new budget."""
    model = Budget
    form_class = BudgetForm
    template_name = 'budgets/budget_form.html'
    success_url = reverse_lazy('budget_list')
    login_url = 'account_login'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        if not form.instance.currency:
            form.instance.currency = self.request.user.profile.preferred_currency
        messages.success(self.request, 'Budget created successfully!')
        return super().form_valid(form)


class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    """Update a budget."""
    model = Budget
    form_class = BudgetForm
    template_name = 'budgets/budget_form.html'
    success_url = reverse_lazy('budget_list')
    login_url = 'account_login'

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Budget updated successfully!')
        return super().form_valid(form)


class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a budget."""
    model = Budget
    template_name = 'budgets/budget_confirm_delete.html'
    success_url = reverse_lazy('budget_list')
    login_url = 'account_login'

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Budget deleted successfully!')
        return super().delete(request, *args, **kwargs)
