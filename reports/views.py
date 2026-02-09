from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.utils.timezone import make_aware
from datetime import datetime
from decimal import Decimal
from transactions.models import Transaction
import calendar


class MonthlyReportView(LoginRequiredMixin, TemplateView):
    """Display monthly income vs expense report."""
    template_name = 'reports/monthly_report.html'
    login_url = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get all transactions for the user, grouped by month
        transactions = Transaction.objects.filter(user=user).order_by('-date')

        # Group by month and calculate totals
        monthly_data = {}

        for transaction in transactions:
            month_key = transaction.date.strftime('%Y-%m')
            month_display = transaction.date.strftime('%B %Y')

            if month_key not in monthly_data:
                monthly_data[month_key] = {
                    'display': month_display,
                    'income': Decimal('0.00'),
                    'expense': Decimal('0.00'),
                    'savings': Decimal('0.00'),
                }

            # Skip if category is null (deleted)
            if not transaction.category:
                continue

            if transaction.category.type == 'income':
                monthly_data[month_key]['income'] += transaction.amount
            else:
                monthly_data[month_key]['expense'] += transaction.amount

            monthly_data[month_key]['savings'] = (
                monthly_data[month_key]['income'] - monthly_data[month_key]['expense']
            )

        # Sort by date descending
        sorted_months = sorted(monthly_data.items(), reverse=True)
        report_data = [
            {
                'month_key': month,
                'month_display': data['display'],
                'income': data['income'],
                'expense': data['expense'],
                'savings': data['savings'],
            }
            for month, data in sorted_months
        ]

        context['report_data'] = report_data
        context['has_data'] = len(report_data) > 0

        # Calculate totals
        if report_data:
            total_income = sum(d['income'] for d in report_data) or Decimal('0.00')
            total_expense = sum(d['expense'] for d in report_data) or Decimal('0.00')
            total_savings = total_income - total_expense

            context.update({
                'total_income': total_income,
                'total_expense': total_expense,
                'total_savings': total_savings,
                'months_count': len(report_data),
            })

        return context


class CategoryReportView(LoginRequiredMixin, TemplateView):
    """Display category-wise expense/income report."""
    template_name = 'reports/category_report.html'
    login_url = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get transactions grouped by category
        transactions = Transaction.objects.filter(user=user)

        # Get all categories with their totals
        from transactions.models import Category

        category_data = []

        for category in Category.objects.filter(user=user):
            total = transactions.filter(category=category).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
            transaction_count = transactions.filter(category=category).count()

            category_data.append({
                'category': category,
                'total': total,
                'transaction_count': transaction_count,
                'type_display': category.get_type_display(),
            })

        # Sort by total descending
        category_data.sort(key=lambda x: x['total'], reverse=True)

        # Separate income and expense
        income_categories = [c for c in category_data if c['category'].type == 'income']
        expense_categories = [c for c in category_data if c['category'].type == 'expense']

        context['income_categories'] = income_categories
        context['expense_categories'] = expense_categories
        context['total_income'] = sum((c['total'] for c in income_categories), Decimal('0.00'))
        context['total_expense'] = sum((c['total'] for c in expense_categories), Decimal('0.00'))
        context['has_data'] = len(category_data) > 0

        return context
