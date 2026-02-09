from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.core.exceptions import ValidationError


class Category(models.Model):
    """Transaction categories for income and expenses."""
    INCOME = 'income'
    EXPENSE = 'expense'

    TYPE_CHOICES = [
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        unique_together = ('user', 'name', 'type')
        verbose_name_plural = 'Categories'
        indexes = [
            models.Index(fields=['user', 'type']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Transaction(models.Model):
    """Income and expense transactions."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='transactions'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]  # Changed: Allow zero now (See requirements)
    )
    date = models.DateField()
    description = models.TextField(blank=True, default='')
    currency = models.CharField(
        max_length=3,
        default='INR',
        help_text='ISO 4217 currency code'
    )
    receipt = models.FileField(
        upload_to='receipts/',
        null=True,
        blank=True,
        help_text='Upload receipt for documentation'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', '-date']),
            models.Index(fields=['user', 'category']),
            models.Index(fields=['date']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(amount__gt=0),
                name='amount_positive'
            )
        ]

    def __str__(self):
        category_name = self.category.get_type_display() if self.category else 'Uncategorized'
        return f"{category_name}: {self.amount} {self.currency} on {self.date}"

    def clean(self):
        """Validate transaction data."""
        if self.amount <= 0:
            raise ValidationError("Amount must be greater than zero.")
        if self.category and self.user_id:  # Check user_id to avoid accessing related object
            if self.category.user_id != self.user_id:
                raise ValidationError("Category must belong to the same user.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
