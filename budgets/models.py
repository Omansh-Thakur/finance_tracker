from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from transactions.models import Category


class Budget(models.Model):
    """Monthly budget limits for expense categories."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.OneToOneField(
        Category,
        on_delete=models.CASCADE,
        related_name='budget'
    )
    monthly_limit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    currency = models.CharField(
        max_length=3,
        default='INR',
        help_text='ISO 4217 currency code'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Budgets'
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"Budget for {self.category.name}: {self.monthly_limit} {self.currency}"

    @property
    def is_exceeded(self):
        """Check if budget is exceeded for current month."""
        from django.utils import timezone
        from django.db.models import Sum

        today = timezone.now().date()
        current_month_start = today.replace(day=1)

        if today.month == 12:
            current_month_end = today.replace(year=today.year + 1, month=1, day=1)
        else:
            current_month_end = today.replace(month=today.month + 1, day=1)

        spent = self.category.transactions.filter(
            date__gte=current_month_start,
            date__lt=current_month_end,
            user=self.user
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        return spent > self.monthly_limit

    def get_spent_amount(self):
        """Get total spent for current month in this category."""
        from django.utils import timezone
        from django.db.models import Sum

        today = timezone.now().date()
        current_month_start = today.replace(day=1)

        if today.month == 12:
            current_month_end = today.replace(year=today.year + 1, month=1, day=1)
        else:
            current_month_end = today.replace(month=today.month + 1, day=1)

        spent = self.category.transactions.filter(
            date__gte=current_month_start,
            date__lt=current_month_end,
            user=self.user
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        return spent

    def get_percentage_used(self):
        """Get percentage of budget used."""
        spent = self.get_spent_amount()
        if self.monthly_limit == 0:
            return Decimal('0.00')
        percentage = (spent / self.monthly_limit) * 100
        return min(percentage, Decimal('100.00'))
