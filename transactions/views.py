from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from transactions.models import Transaction, Category
from transactions.forms import TransactionForm, CategoryForm, TransactionFilterForm


class CategoryListView(LoginRequiredMixin, ListView):
    """List all categories for the user."""
    model = Category
    template_name = 'transactions/category_list.html'
    context_object_name = 'categories'
    paginate_by = 20
    login_url = 'account_login'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).order_by('type', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['income_categories'] = Category.objects.filter(
            user=self.request.user,
            type='income'
        ).count()
        context['expense_categories'] = Category.objects.filter(
            user=self.request.user,
            type='expense'
        ).count()
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    """Create a new category."""
    model = Category
    form_class = CategoryForm
    template_name = 'transactions/category_form.html'
    success_url = reverse_lazy('category_list')
    login_url = 'account_login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Category created successfully!')
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    """Update a category."""
    model = Category
    form_class = CategoryForm
    template_name = 'transactions/category_form.html'
    success_url = reverse_lazy('category_list')
    login_url = 'account_login'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully!')
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a category."""
    model = Category
    template_name = 'transactions/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')
    login_url = 'account_login'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Category deleted successfully! Associated transactions are safe.')
        return super().delete(request, *args, **kwargs)


class TransactionListView(LoginRequiredMixin, ListView):
    """List all transactions for the user with filtering."""
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 20
    login_url = 'account_login'

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user).select_related('category').order_by('-date')

        # Apply filters
        category = self.request.GET.get('category')
        month = self.request.GET.get('month')
        year = self.request.GET.get('year')
        trans_type = self.request.GET.get('type')

        if category:
            queryset = queryset.filter(category_id=category)

        if month:
            queryset = queryset.filter(date__month=month)

        if year:
            queryset = queryset.filter(date__year=year)

        if trans_type:
            queryset = queryset.filter(category__type=trans_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TransactionFilterForm(
            self.request.GET,
            user=self.request.user
        )
        return context


class TransactionDetailView(LoginRequiredMixin, DetailView):
    """View transaction details."""
    model = Transaction
    template_name = 'transactions/transaction_detail.html'
    context_object_name = 'transaction'
    login_url = 'account_login'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class TransactionCreateView(LoginRequiredMixin, CreateView):
    """Create a new transaction."""
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transaction_list')
    login_url = 'account_login'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        if not form.instance.currency:
            form.instance.currency = self.request.user.profile.preferred_currency
        if not form.instance.date:
            form.instance.date = timezone.now().date()
        messages.success(self.request, 'Transaction created successfully!')
        return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    """Update a transaction."""
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transaction_list')
    login_url = 'account_login'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Transaction updated successfully!')
        return super().form_valid(form)


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a transaction."""
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction_list')
    login_url = 'account_login'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Transaction deleted successfully!')
        return super().delete(request, *args, **kwargs)
